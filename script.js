const topbar = document.querySelector("[data-topbar]");
const yearNode = document.querySelector("#current-year");
const workflowCopy = document.querySelector("[data-workflow-copy]");
const flowNodes = Array.from(document.querySelectorAll(".flow-node"));

const workflowText = {
  idea: "Start with a campaign brief, then expand it into scripts, references, images, video, sound, and finished outputs without leaving the canvas.",
  script: "Shape the creative direction into scenes, prompts, ad copy, and production notes before generating visual assets.",
  image: "Create reference frames, product compositions, posters, and social-ready visuals while keeping the source idea connected.",
  video: "Turn selected frames and scripts into motion output for ads, short films, campaign tests, and creator content."
};

if (yearNode) {
  yearNode.textContent = new Date().getFullYear();
}

const handleScroll = () => {
  if (!topbar) return;
  topbar.classList.toggle("is-scrolled", window.scrollY > 12);
};

flowNodes.forEach((node) => {
  node.addEventListener("click", () => {
    flowNodes.forEach((entry) => entry.classList.remove("is-active"));
    node.classList.add("is-active");
    if (workflowCopy) {
      workflowCopy.textContent = workflowText[node.dataset.node] || workflowText.idea;
    }
  });
});

window.addEventListener("scroll", handleScroll, { passive: true });
handleScroll();
