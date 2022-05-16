﻿using System;
using System.IO;
using System.Net;
using System.Net.Http;
using System.Reflection;
using System.Threading;
using System.Windows.Media.Imaging;

namespace iPhoto.UtilityClasses
{
    public static class DataHandler
    {
        public static string GetSideMenuIconsDirectoryPath()
        {
            return GetProjectDirectoryPath() + "\\Graphics\\Icons\\";
        }
        public static string GetAlbumIconsDirectoryPath()
        {
            return GetProjectDirectoryPath() + "\\Graphics\\AlbumIcons\\";
        }
        public static string GetProjectDirectoryPath()
        {
            var path = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location)!.Split('\\');
            int length = 0;

            for (int i = 0; i < path.Length; i++)
            {
                length += 1;
                if (path[i] == "iPhoto")
                {
                    break;
                }
            }

            return String.Join("\\", path, 0, length);
        }
        public static string GetDatabaseDirectory()
        {
            return GetProjectDirectoryPath() + "\\DataBase";
        }
        public static string GetDatabaseImageDirectory()
        {
            return GetProjectDirectoryPath() + "\\DataBase\\Images";
        }
        public static BitmapImage LoadBitmapImage(string path, double? decodePixelWidth)
        {
            BitmapImage image = new BitmapImage();

            image.BeginInit();
            image.UriSource = new Uri(path);
            image.CacheOption = BitmapCacheOption.OnLoad;
            if (decodePixelWidth != null)
            {
                image.DecodePixelWidth = (int)decodePixelWidth;
            }
            image.EndInit();

            image.Freeze();

            return image;
        }
        public static BitmapImage LoadBitmapImageAsync(string path, double? decodePixelWidth)
        {
            var webClient = new WebClient();
            byte[] imageBytes = webClient.DownloadData(path);
            Stream stream = new MemoryStream(imageBytes);

            var bitmapImage = new BitmapImage();
            bitmapImage.BeginInit();
            bitmapImage.StreamSource = stream;
            bitmapImage.CacheOption = BitmapCacheOption.OnLoad;

            if (decodePixelWidth != null)
            {
                bitmapImage.DecodePixelWidth = (int)decodePixelWidth;
            }


            var client = new HttpClient();

            bitmapImage.EndInit();

            return bitmapImage;
        }
    }
}
