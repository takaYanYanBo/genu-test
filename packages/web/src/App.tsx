import React, { useMemo, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { PiList, PiHouse, PiGear, PiX, PiRobot } from 'react-icons/pi';
import { Outlet } from 'react-router-dom';
import Drawer, { ItemProps } from './components/Drawer';
import ButtonIcon from './components/ButtonIcon';
import '@aws-amplify/ui-react/styles.css';
import useDrawer from './hooks/useDrawer';
import useScreen from './hooks/useScreen';
import { useTranslation } from 'react-i18next';

const App: React.FC = () => {
  const { t } = useTranslation();
  const { switchOpen: switchDrawer, opened: isOpenDrawer } = useDrawer();
  const { pathname } = useLocation();
  const { screen, notifyScreen, scrollTopAnchorRef, scrollBottomAnchorRef } =
    useScreen();

  const items: ItemProps[] = [
    {
      label: t('navigation.home'),
      to: '/',
      icon: <PiHouse />,
      display: 'usecase' as const,
    },
    {
      label: t('navigation.settings'),
      to: '/setting',
      icon: <PiGear />,
      display: 'none' as const,
    },
    {
      label: t('agent_core.title'),
      to: '/agent-core',
      icon: <PiRobot />,
      display: 'usecase' as const,
    },
  ];

  const label = useMemo(() => {
    return items.find((i) => i.to === pathname)?.label || '';
  }, [items, pathname]);

  useEffect(() => {
    if (screen.current) {
      notifyScreen(screen.current);
    }
  }, [pathname, screen, notifyScreen]);

  return (
    <div
      className="screen:w-screen screen:h-screen overflow-x-hidden overflow-y-scroll"
      ref={screen}>
      <main className="flex-1">
        <div ref={scrollTopAnchorRef}></div>
        <header className="bg-aws-squid-ink visible flex h-12 w-full items-center justify-between text-lg text-white lg:invisible lg:h-0 print:hidden">
          <div className="flex w-10 items-center justify-start">
            <button
              className="focus:ring-aws-sky mr-2 rounded-full  p-2 hover:opacity-50 focus:outline-none focus:ring-1"
              onClick={() => {
                switchDrawer();
              }}>
              <PiList />
            </button>
          </div>

          {label}

          {/* Dummy block to center the label */}
          <div className="w-10" />
        </header>

        <div
          className={`fixed -left-64 top-0 z-50 transition-all lg:left-0 lg:z-0 ${
            isOpenDrawer ? 'left-0' : '-left-64'
          }`}>
          <Drawer items={items} />
        </div>

        <div
          id="smallDrawerFiller"
          className={`${isOpenDrawer ? 'visible' : 'invisible'} lg:invisible`}>
          <div
            className="screen:h-screen fixed top-0 z-40 w-screen bg-gray-900/90"
            onClick={switchDrawer}></div>
          <ButtonIcon
            className="fixed left-64 top-0 z-40 text-white"
            onClick={switchDrawer}>
            <PiX />
          </ButtonIcon>
        </div>
        <div className="text-aws-font-color lg:ml-64">
          <Outlet />
        </div>
        <div ref={scrollBottomAnchorRef}></div>
      </main>
    </div>
  );
};

export default App;
