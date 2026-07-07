import { NavLink } from 'react-router-dom';

const Sidebar = () => {
  return (
    <nav className="fixed left-0 top-16 h-[calc(100vh-64px)] w-60 flex flex-col p-md bg-surface-container-low dark:bg-inverse-surface border-r border-outline-variant dark:border-outline z-40 hidden md:flex">
      <div className="mb-xl px-sm">
        <h2 className="font-headline-md text-headline-md font-bold text-primary">Clinical Portal</h2>
        <p className="font-label-md text-label-md text-secondary mt-1">Station 04 - Online</p>
      </div>
      <button className="w-full flex items-center justify-center gap-2 bg-primary text-on-primary py-2 px-4 rounded-lg font-label-md text-label-md mb-lg hover:bg-primary-container hover:text-on-primary-container transition-colors shadow-sm">
        <span className="material-symbols-outlined text-[18px]">add</span>
        New Triage
      </button>
      <ul className="flex-1 space-y-2">
        <li>
          <NavLink to="/" className={({isActive}) => `flex items-center gap-3 px-3 py-2 rounded-lg transition-all active:scale-95 duration-150 ${isActive ? 'bg-secondary-container text-on-secondary-container font-semibold' : 'text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant'}`}>
            <span className="material-symbols-outlined">dashboard</span>
            <span className="font-label-md text-label-md">Dashboard</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/intake" className={({isActive}) => `flex items-center gap-3 px-3 py-2 rounded-lg transition-all active:scale-95 duration-150 ${isActive ? 'bg-secondary-container text-on-secondary-container font-semibold' : 'text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant'}`}>
            <span className="material-symbols-outlined">person_add</span>
            <span className="font-label-md text-label-md">Patient Intake</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/analysis" className={({isActive}) => `flex items-center gap-3 px-3 py-2 rounded-lg transition-all active:scale-95 duration-150 ${isActive ? 'bg-secondary-container text-on-secondary-container font-semibold' : 'text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant'}`}>
            <span className="material-symbols-outlined">mic</span>
            <span className="font-label-md text-label-md">Cough Analysis</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/history" className={({isActive}) => `flex items-center gap-3 px-3 py-2 rounded-lg transition-all active:scale-95 duration-150 ${isActive ? 'bg-secondary-container text-on-secondary-container font-semibold' : 'text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant'}`}>
            <span className="material-symbols-outlined">history</span>
            <span className="font-label-md text-label-md">Triage History</span>
          </NavLink>
        </li>
      </ul>
      <div className="mt-auto border-t border-outline-variant pt-4 space-y-2">
        <a className="flex items-center gap-3 px-3 py-2 text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant rounded-lg transition-all" href="#">
          <span className="material-symbols-outlined">help</span>
          <span className="font-label-md text-label-md">Support</span>
        </a>
        <a className="flex items-center gap-3 px-3 py-2 text-secondary dark:text-secondary-fixed-dim hover:bg-error-container hover:text-on-error-container rounded-lg transition-all" href="#">
          <span className="material-symbols-outlined">logout</span>
          <span className="font-label-md text-label-md">Logout</span>
        </a>
      </div>
    </nav>
  );
};

export default Sidebar;
