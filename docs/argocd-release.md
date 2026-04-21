# TapNow ArgoCD Release Notes

Production route:

- GitHub repository: `gateszhangc/tapnow`
- Git branch: `main`
- Dokploy project: `N/A`
- Registry image: `ghcr.io/gateszhangc/tapnow:<git-sha>`
- GitOps repository: `gateszhangc/tapnow-gitops`
- GitOps path: `apps/tapnow/overlays/prod`
- ArgoCD application: `tapnow-prod`

## Required GitHub Actions secrets

- `KUBE_CONFIG_DATA`: base64-encoded kubeconfig for the build cluster
- `GITOPS_PAT`: token with push access to `gateszhangc/tapnow-gitops`

The workflow uses its built-in `GITHUB_TOKEN` for source checkout inside the cluster build job and for pushing the image to GHCR.

## Release flow

1. `main` receives a push.
2. GitHub Actions runs Playwright browser tests.
3. GitHub Actions applies `deploy/build-job.yaml` into the `build-jobs` namespace.
4. The build job clones the app repo at the pushed commit and builds `ghcr.io/gateszhangc/tapnow:<git-sha>` with Kaniko.
5. GitHub Actions checks out `gateszhangc/tapnow-gitops` and updates `apps/tapnow/overlays/prod/kustomization.yaml`.
6. ArgoCD auto-syncs `tapnow-prod` and rolls the deployment in namespace `tapnow-prod`.

## Bootstrap order

1. Create the GitHub repositories `gateszhangc/tapnow` and `gateszhangc/tapnow-gitops`.
2. Push this application repo to `gateszhangc/tapnow`.
3. Copy `gitops/apps` and `gitops/argocd` from this repo into `gateszhangc/tapnow-gitops`.
4. Apply `gitops/argocd/tapnow-prod.yaml` to the cluster where ArgoCD runs.
5. Add the required GitHub Actions secrets.
6. Create `ghcr-pull-secret` in namespace `tapnow-prod` so the cluster can pull the private GHCR image.
7. Point DNS for `tapnow.lol` to the production ingress.
