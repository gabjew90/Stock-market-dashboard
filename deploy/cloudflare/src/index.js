// seraphsys.us — static dashboard site + server-side pulse-data proxy.
// The proxy keeps the upstream GitHub source invisible to visitors:
// browsers only ever talk to seraphsys.us.

const UPSTREAM = "https://raw.githubusercontent.com/gabjew90/Institutional-report-bot/pulse-data/pulse-output/web";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname.startsWith("/pulse-data/")) {
      const rest = url.pathname.slice("/pulse-data/".length);
      // Only expose the two shapes the pulse page needs.
      const allowed = rest === "archive.json" || /^fragments\/[\w.-]+\.html$/.test(rest);
      if (!allowed) return new Response("Not found", { status: 404 });

      const upstream = await fetch(`${UPSTREAM}/${rest}`, {
        // Cache successes for 5 min; never cache failures — a transient
        // upstream blip must not get pinned at the edge.
        cf: { cacheEverything: true, cacheTtlByStatus: { "200-299": 300, "300-599": -1 } },
      });
      if (!upstream.ok) {
        return new Response("upstream unavailable", {
          status: 503,
          headers: { "cache-control": "no-store" },
        });
      }
      const headers = new Headers();
      headers.set("content-type", upstream.headers.get("content-type") || (rest.endsWith(".json") ? "application/json" : "text/html; charset=utf-8"));
      headers.set("cache-control", "public, max-age=300");
      // Deliberately no upstream headers passed through — nothing identifying leaks.
      return new Response(upstream.body, { status: upstream.status, headers });
    }

    return env.ASSETS.fetch(request);
  },
};
