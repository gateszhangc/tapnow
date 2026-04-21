# TapNow GitOps Bootstrap

This directory is the bootstrap payload for the separate GitOps repository `gateszhangc/tapnow-gitops`.

Expected production route:

- GitHub repository: `gateszhangc/tapnow`
- Git branch: `main`
- Dokploy project: `N/A` for this setup
- GitOps repository: `gateszhangc/tapnow-gitops`
- ArgoCD application: `tapnow-prod`

Copy `apps/` and `argocd/` into the root of the GitOps repo before enabling the release workflow in the application repo.
