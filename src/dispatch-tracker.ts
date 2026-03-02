// pinkflow/src/github/dispatch-tracker.ts
export class GitHubDispatchTracker {
  /**
   * GitHub's API doesn't return the workflow run ID when you dispatch.
   * This solves that by embedding a unique ID in the workflow input,
   * then searching for that ID in step names across recent runs.
   */
  
  async dispatchAndTrack(
    client: GitHubClient,
    org: string,
    repo: string,
    workflowFile: string,
    ref: string,
    inputs: Record<string, any>
  ): Promise<{ runId: number; dispatchId: string }> {
    
    // Generate deterministic ID for this attempt
    const dispatchId = this.generateDispatchId();
    
    // Trigger with our ID in the inputs
    await client.actions.createWorkflowDispatch({
      owner: org,
      repo,
      workflow_id: workflowFile,
      ref,
      inputs: {
        ...inputs,
        dispatch_id: dispatchId  // CRITICAL
      }
    });
    
    // Wait for the run to appear (GitHub is eventually consistent)
    await this.delay(3000);
    
    // Search for our ID in step names
    const runId = await this.findRunIdByDispatchId(
      client, org, repo, workflowFile, dispatchId
    );
    
    return { runId, dispatchId };
  }
  
  private async findRunIdByDispatchId(
    client: GitHubClient,
    org: string,
    repo: string,
    workflowFile: string,
    dispatchId: string
  ): Promise<number> {
    // List recent runs
    const runs = await client.actions.listWorkflowRuns({
      owner: org,
      repo,
      workflow_id: workflowFile,
      per_page: 10
    });
    
    // For each run, check its jobs for our step name
    for (const run of runs.data.workflow_runs) {
      const jobs = await client.actions.listJobsForWorkflowRun({
        owner: org,
        repo,
        run_id: run.id
      });
      
      for (const job of jobs.data.jobs) {
        for (const step of job.steps) {
          if (step.name.includes(dispatchId)) {
            return run.id;
          }
        }
      }
    }
    
    throw new Error(`Could not find workflow run with dispatch ID: ${dispatchId}`);
  }
  
  private generateDispatchId(): string {
    // Format: pinkflow-{timestamp}-{random}
    return `pinkflow-${Date.now()}-${Math.random().toString(36).substring(2, 8)}`;
  }
}