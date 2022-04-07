﻿using iPhoto.Commands;
using System.Windows;

namespace iPhoto.ViewModels
{
    public class MainWindowViewModel : ViewModelBase
    {
        private MainWindow? _mainWindow;

        private ViewModelBase? _mainViewModel;
        public ViewModelBase MainViewModel
        {
            get
            {
                return _mainViewModel;
            }
            set
            {
                _mainViewModel = value;
                OnPropertyChanged(nameof(MainViewModel));
            }
        }
        public SearchViewModel SearchViewModel { get; }
        public AlbumsViewModel AlbumsViewModel { get; }
        public AccountViewModel AccountViewModel { get; }
        public SettingsViewModel SettingsViewModel { get; }
        public HomePageViewModel HomePageViewModel { get; }

        public MainWindowViewModel(Window mainWindow)
        {
            HomePageViewModel = new HomePageViewModel();
            SearchViewModel = new SearchViewModel();
            AlbumsViewModel = new AlbumsViewModel();
            AccountViewModel = new AccountViewModel();
            SettingsViewModel = new SettingsViewModel();
            
            BindMainWindow(mainWindow);

            MainViewModel = HomePageViewModel;
        }
        private void BindMainWindow(Window mainWindow)
        {
            _mainWindow = mainWindow as MainWindow;

            var sideMenuDataContext = _mainWindow.sideMenu.DataContext as SideMenuViewModel;

            sideMenuDataContext.NavigateCommand = new NavigateCommand(this);
        }
    }
}