import { Outlet } from 'react-router-dom';
import Header from './Header';
import Sidebar from './Sidebar';

const Layout = () => {
  return (
    <>
      <Header />
      <Sidebar />
      <main className="pt-16 md:pl-60 w-full min-h-screen">
        <Outlet />
      </main>
    </>
  );
};

export default Layout;
