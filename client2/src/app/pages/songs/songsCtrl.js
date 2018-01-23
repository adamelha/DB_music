/**
 * @author v.lugovsky
 * created on 16.12.2015
 */
(function () {
    'use strict';

    angular.module('BlurAdmin.pages.songs')
        .controller('songsCtrl', songsCtrl);

    /** @ngInject */
    function songsCtrl($scope, $filter, editableOptions, editableThemes, $uibModal, $timeout, $q, ServerConnection) {

        let tableFields = [
            {
                name: 'name',
                alias: 'Name',
                label: 'Name',
                placeholder: 'Name',
            },
            {
                name: 'album',
                alias: 'Album',
                label: 'Album',
                placeholder: 'Album'
            },
            {
                name: 'artist',
                alias: 'Artist',
                label: 'Artist',
                placeholder: 'Artist'
            }
        ];
        $scope.playlists = [{name: 'a'}, {name: 'b'}, {name: 'c'}, {name: 'd'}, {name: 'eeeeeeeeeefasdfasdfasdfasdf'}]
        $scope.text = {}
        $scope.updateSelect = (playlist) => {
            ServerConnection.sendPost('/addToPlaylist', {
                playlist_name: playlist.name,
                track_id: $scope.songId
            }).then((r) => {

            })

        }

        $scope.onChange = (text) => {
            // if (newVal != null && newVal != undefined && newVal != oldVal) {
            //     returnMock()
            ServerConnection.sendPost('/searchPlaylist', {search: text}).then((r) => {
                $scope.playlists = r.list;
            })
            // }
        }

        function returnMock() {
            let d = $q.defer();
            $timeout(() => {
                let items = $scope.mockItems || [];
                d.resolve({total_rows: items.length, list: items})
            }, 0);
            return d.promise;
        }

        function showModal(song) {
            $scope.songId = song.track_id;
            $uibModal.open({
                animation: true,
                templateUrl: 'app/pages/songs/addToPlaylist.modal.html',
                size: 'sm',
                scope: $scope,
                resolve: {
                    items: function () {
                        return $scope.items;
                    }
                }
            });
        }

        $scope.rightColumn = {
            name: 'Add To Playlist',
            buttons: [
                {
                    onClick: (row) => {
                        // let shouldBeOpen = !row.menuOpen;
                        // $scope.songs.forEach(s => s.menuOpen = false);
                        // row.menuOpen = shouldBeOpen;
                        showModal(row);
                        // ServerConnection.sendPost('/removePlaylist', {playlist_name: row.name}) //TODO - add unique identifier for playlist
                    },
                    icon: 'fa fa-list',
                    isShownOnRow: () => {
                        return true
                    }
                }
            ]
        }

        function postProcess(songs) {
            $scope.songs = songs;
            return songs;
        }

        $scope.updateSongs=(lyrics)=>{
            let options = $scope.tableConfig.reqOtions ? $scope.tableConfig.reqOtions : null;
            if (options){
                options.filters.lyrics=lyrics;
            }
            else{
                options={filters:{lyrics:lyrics}}
            }

            ServerConnection.sendPost('/songs', options).then((r) => {
                $scope.lyrics='';
            },err=>{
                $scope.lyrics='';
            })
        }

        $scope.tableConfig = {
            path: '/songs',
            postProcess: postProcess.bind({$scope: $scope}),
            options: {
                filter: {}
            },
            fields: tableFields
        }

        $scope.items = [
            {
                name: 'item1',
                album: 'album1',
                artist: 'artist1',
            },
            {
                name: 'item2',
                album: 'album2',
                artist: 'artist2',
            }
        ]

    }

})();
