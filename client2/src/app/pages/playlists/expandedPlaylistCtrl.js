/**
 * @author v.lugovsky
 * created on 16.12.2015
 */
(function () {
    'use strict';

    angular.module('BlurAdmin.pages.playlists')
        .controller('expandedPlaylistCtrl', expandedPlaylistCtrl);

    /** @ngInject */
    function expandedPlaylistCtrl($scope,$state, $filter, editableOptions, editableThemes,ServerConnection,$stateParams ) {

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

        $scope.tableConfig = {
            path: '/songs',
            //  postProcess: postProcess.bind({$scope: $scope}),
            options: {
                filter: {playlist_name:$stateParams.playlistName}
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

        $scope.leftColumn = {
            name: 'Delete',
            buttons: [
                {
                    onClick: (row) => {
                        ServerConnection.sendPost('/removeSongFromPlaylist', {playlist_name: $stateParams.playlistName, track_id:row.track_id})
                    },
                    icon: 'fa fa-remove',
                    isShownOnRow: () => {
                        return true
                    }
                }
            ]
        }



    }

})();
