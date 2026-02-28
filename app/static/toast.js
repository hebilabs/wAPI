const ToastManager = {
  container: null,

  init() {
    if (!this.container) {
      this.container = document.createElement("div");
      this.container.id = "wapi-toast-wrapper";
      this.container.className =
        "fixed bottom-6 right-6 z-[999] flex flex-col gap-4 items-end";
      document.body.appendChild(this.container);
    }
  },

  /**
   * @param {Object} options
   * @param {string} options.type - 'success', 'error', 'info'
   * @param {string|HTMLElement} options.content - String or DOM element
   * @param {number} options.duration - ms before auto-close
   */
  show({ type = "success", content, duration = 4000 }) {
    this.init();

    const toast = document.createElement("div");

    const baseClasses =
      "transform translate-x-full opacity-0 transition-all duration-500 ease-out bg-black text-white p-5 shadow-2xl border-l-4 min-w-[320px] max-w-md flex items-center justify-between group";
    const typeClasses = type === "error" ? "border-red-600" : "border-zinc-500";

    toast.className = `${baseClasses} ${typeClasses}`;

    const contentWrapper = document.createElement("div");
    contentWrapper.className = "flex-1 pr-4";

    if (typeof content === "string") {
      contentWrapper.innerHTML = content;
    } else {
      contentWrapper.appendChild(content);
    }

    const closeBtn = document.createElement("button");
    closeBtn.innerHTML = "✕";
    closeBtn.className =
      "text-[10px] text-zinc-500 hover:text-white transition-colors uppercase font-bold";
    closeBtn.onclick = () => this.hide(toast);

    toast.appendChild(contentWrapper);
    toast.appendChild(closeBtn);
    this.container.appendChild(toast);

    requestAnimationFrame(() => {
      toast.classList.remove("translate-x-full", "opacity-0");
    });

    if (duration > 0) {
      setTimeout(() => this.hide(toast), duration);
    }
  },

  hide(toast) {
    toast.classList.add("translate-x-full", "opacity-0");
    toast.addEventListener("transitionend", () => toast.remove());
  },
};
