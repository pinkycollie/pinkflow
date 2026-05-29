import { serve } from "https://deno.land/std/http/server.ts";
import { encode as btoa } from "https://deno.land/std/encoding/base64.ts";

const GITHUB_CLIENT_ID = Deno.env.get("GITHUB_CLIENT_ID");
const GITHUB_CLIENT_SECRET = Deno.env.get("GITHUB_CLIENT_SECRET");

serve(async (req) => {
  const url = new URL(req.url);
  if (url.pathname === "/auth/github/callback") {
    const code = url.searchParams.get("code");

    const tokenResponse = await fetch("https://github.com/login/oauth/access_token", {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: new URLSearchParams({
        client_id: GITHUB_CLIENT_ID,
        client_secret: GITHUB_CLIENT_SECRET,
        code,
      }),
    });

    const { access_token } = await tokenResponse.json();
    const user = await fetch("https://api.github.com/user", {
      headers: {
        Authorization: `Bearer ${access_token}`
      },
    }).then(res => res.json());

    return Response.json({
      message: "GitHub Auth Success",
      user,
    });
  }

  return new Response("Hello from PinkFlow!", { status: 200 });
});