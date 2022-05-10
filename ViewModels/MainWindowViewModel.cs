﻿using iPhoto.Commands;
using System.Windows;
using iPhoto.DataBase;
using iPhoto.Views.SearchPage;
using iPhoto.ViewModels.AlbumsPage;

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
        public PlacesViewModel PlacesViewModel { get; }
        public AccountViewModel AccountViewModel { get; }
        public SettingsViewModel SettingsViewModel { get; }
        public HomePageViewModel HomePageViewModel { get; }

        //MG 15.04 added db handler class
        public MainWindowViewModel(Window mainWindow, DatabaseHandler database, PhotoDetailsWindowView photoDetailsWindow)
        {
            HomePageViewModel = new HomePageViewModel();
            SearchViewModel = new SearchViewModel(database, photoDetailsWindow);    //MG 15.04 //MG 26.04 add photo details 
            AlbumsViewModel = new AlbumsViewModel(database, this, photoDetailsWindow);
            PlacesViewModel = new PlacesViewModel();
            AccountViewModel = new AccountViewModel();
            SettingsViewModel = new SettingsViewModel();


            BindMainWindow(mainWindow);

            MainViewModel = HomePageViewModel;
        }
        private void BindMainWindow(Window mainWindow)
        {
            _mainWindow = mainWindow as MainWindow;

            var sideMenuDataContext = _mainWindow!.sideMenu.DataContext as SideMenuViewModel;

            sideMenuDataContext!.NavigateCommand = new NavigateCommand(this);
        }
    }
}