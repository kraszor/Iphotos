﻿using iPhoto.DataBase;
using iPhoto.ViewModels;
using iPhoto.ViewModels.AlbumsPage;
using iPhoto.Views.SearchPage;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace iPhoto.Commands.AlbumPage
{
    public class ShowAlbumContentCommand : CommandBase
    {
        private readonly MainWindowViewModel _mainWindowViewModel;
        private readonly Album _album;
        private readonly DatabaseHandler _database;
        private readonly PhotoDetailsWindowView _photoDetailsWindow;
        public ShowAlbumContentCommand(DatabaseHandler database, PhotoDetailsWindowView photoDetailsWindow, MainWindowViewModel mainWindowViewModel, Album album)
        {
            _mainWindowViewModel = mainWindowViewModel;
            _album = album;
            _database = database;
            _photoDetailsWindow = photoDetailsWindow;

        }
        public override void Execute(object parameter)
        {
            _mainWindowViewModel.MainViewModel = new AlbumContentViewModel(_database, _photoDetailsWindow, _mainWindowViewModel, _album);
        }
    }
}