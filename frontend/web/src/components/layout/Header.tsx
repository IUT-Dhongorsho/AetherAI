

const Header = () => {
  return (
    <header className="fixed top-0 left-0 w-full z-50 flex justify-between items-center px-lg h-16 bg-surface dark:bg-on-surface-variant border-b border-outline-variant dark:border-outline">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-sm">
          <span className="material-symbols-outlined text-primary dark:text-primary-fixed-dim icon-fill font-headline-lg text-headline-lg">hub</span>
          <h1 className="font-headline-lg text-headline-lg font-bold text-primary dark:text-primary-fixed-dim tracking-tight">AetherAI</h1>
        </div>
        <div className="hidden md:flex items-center gap-2 px-3 py-1 bg-surface-container rounded-full border border-outline-variant ml-4">
          <div aria-label="Status Online" className="w-2 h-2 rounded-full bg-primary"></div>
          <span className="font-label-md text-label-md text-on-surface-variant">System Online</span>
        </div>
      </div>
      <div className="flex items-center gap-4">
        <button className="p-2 text-secondary dark:text-secondary-fixed-dim hover:bg-surface-container dark:hover:bg-surface-container-highest transition-colors rounded-full cursor-pointer active:opacity-80">
          <span className="material-symbols-outlined">sensors</span>
        </button>
        <button className="p-2 text-secondary dark:text-secondary-fixed-dim hover:bg-surface-container dark:hover:bg-surface-container-highest transition-colors rounded-full cursor-pointer active:opacity-80">
          <span className="material-symbols-outlined">settings</span>
        </button>
        <button className="p-2 text-secondary dark:text-secondary-fixed-dim hover:bg-surface-container dark:hover:bg-surface-container-highest transition-colors rounded-full cursor-pointer active:opacity-80">
          <span className="material-symbols-outlined">account_circle</span>
        </button>
      </div>
    </header>
  );
};

export default Header;
