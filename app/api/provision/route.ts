import { Octokit } from 'octokit';
import { NextRequest, NextResponse } from 'next/server';

interface ProvisionRequest {
  customerEmail: string;
  plan: string;
  templateRepo: string;
  priceId: string;
}

async function createGitHubInstallationToken() {
  // In production, use GitHub App private key to create installation token
  // For now, we'll use a personal access token or installation token
  return process.env.GH_APP_INSTALLATION_TOKEN || process.env.GITHUB_TOKEN;
}

async function setRepoSecret(
  octokit: Octokit,
  owner: string,
  repo: string,
  secretName: string,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  _secretValue: string
) {
  // Get repository public key for encrypting secrets
  try {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { data: _publicKey } = await octokit.rest.actions.getRepoPublicKey({
      owner,
      repo,
    });

    // In production, encrypt the secret value using the public key
    // For now, this is a placeholder
    console.log(`Would set secret ${secretName} for ${owner}/${repo}`);
    
    // await octokit.rest.actions.createOrUpdateRepoSecret({
    //   owner,
    //   repo,
    //   secret_name: secretName,
    //   encrypted_value: encryptedValue,
    //   key_id: publicKey.key_id,
    // });
  } catch (error) {
    console.error(`Failed to set secret ${secretName}:`, error);
  }
}

async function createVercelProject(
  repoName: string,
  gitUrl: string,
  envVars: Record<string, string>
) {
  // Check if Vercel integration is enabled
  const vercelEnabled = process.env.ENABLE_VERCEL_DEPLOY === 'true';
  const vercelToken = process.env.VERCEL_TOKEN;
  const vercelOrgId = process.env.VERCEL_ORG_ID;

  if (!vercelEnabled) {
    console.log('Vercel deployment is disabled');
    return null;
  }

  if (!vercelToken || !vercelOrgId) {
    console.warn('Vercel credentials not configured');
    return null;
  }

  try {
    // Create Vercel project
    const createResponse = await fetch('https://api.vercel.com/v10/projects', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${vercelToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: repoName,
        framework: 'nextjs',
        gitRepository: {
          type: 'github',
          repo: gitUrl,
        },
      }),
    });

    if (!createResponse.ok) {
      const error = await createResponse.text();
      console.error('Failed to create Vercel project:', error);
      return null;
    }

    const project = await createResponse.json();
    console.log('Created Vercel project:', project.id);

    // Set environment variables
    for (const [key, value] of Object.entries(envVars)) {
      await fetch(
        `https://api.vercel.com/v10/projects/${project.id}/env`,
        {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${vercelToken}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            key,
            value,
            type: 'encrypted',
            target: ['production', 'preview'],
          }),
        }
      );
    }

    // Trigger first deployment
    const deployResponse = await fetch(
      `https://api.vercel.com/v13/deployments`,
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${vercelToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: repoName,
          project: project.id,
          gitSource: {
            type: 'github',
            repo: gitUrl,
            ref: 'main',
          },
        }),
      }
    );

    if (!deployResponse.ok) {
      console.error('Failed to trigger deployment');
      return project;
    }

    const deployment = await deployResponse.json();
    console.log('Triggered deployment:', deployment.url);

    return {
      projectId: project.id,
      deploymentUrl: deployment.url,
    };
  } catch (error) {
    console.error('Vercel project creation failed:', error);
    return null;
  }
}

export async function POST(req: NextRequest) {
  try {
    const body: ProvisionRequest = await req.json();
    const { customerEmail, plan, templateRepo } = body;

    if (!customerEmail || !plan || !templateRepo) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      );
    }

    const token = await createGitHubInstallationToken();
    if (!token) {
      return NextResponse.json(
        { error: 'GitHub authentication not configured' },
        { status: 500 }
      );
    }

    const octokit = new Octokit({ auth: token });
    const repoName = `${plan}-${Date.now()}`;
    const templateOwner = process.env.GH_TEMPLATE_OWNER!;
    const targetOwner = process.env.GH_TARGET_OWNER!;

    // 1) Create repository from template
    console.log(`Creating repo ${repoName} from ${templateOwner}/${templateRepo}`);
    
    const { data: newRepo } = await octokit.request(
      'POST /repos/{template_owner}/{template_repo}/generate',
      {
        template_owner: templateOwner,
        template_repo: templateRepo,
        owner: targetOwner,
        name: repoName,
        private: true,
        description: `Auto-provisioned ${plan} app for ${customerEmail}`,
      }
    );

    console.log(`Created repository: ${newRepo.full_name}`);

    // 2) Set repository secrets (optional if using Vercel Git Integration)
    await setRepoSecret(
      octokit,
      targetOwner,
      repoName,
      'NEXT_PUBLIC_APP_NAME',
      process.env.NEXT_PUBLIC_APP_NAME || 'JobMagician'
    );

    await setRepoSecret(
      octokit,
      targetOwner,
      repoName,
      'FIBONROSE_BASE_URL',
      process.env.FIBONROSE_BASE_URL || ''
    );

    // 3) Create Vercel project and deploy (optional)
    const vercelResult = await createVercelProject(repoName, newRepo.html_url, {
      NEXT_PUBLIC_APP_NAME: process.env.NEXT_PUBLIC_APP_NAME || 'JobMagician',
      FIBONROSE_BASE_URL: process.env.FIBONROSE_BASE_URL || '',
      PLAN: plan,
      CUSTOMER_EMAIL: customerEmail,
    });

    // 4) Return results
    return NextResponse.json({
      success: true,
      repo: newRepo.html_url,
      repoName,
      deploymentUrl: vercelResult?.deploymentUrl || null,
      message: 'Repository provisioned successfully',
    });
  } catch (err) {
    const error = err as Error;
    console.error('Provisioning error:', error);
    return NextResponse.json(
      { error: 'Failed to provision repository', details: error.message },
      { status: 500 }
    );
  }
}
