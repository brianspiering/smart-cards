var app = angular.module('StarterApp', ['ngMaterial']);
var BASE_URL = "http://127.0.0.1:5000/"
app.config(function($mdIconProvider) {
  /**
   * Load icon sets to get different svg icons
   */
  $mdIconProvider
    .iconSet('action', 'https://raw.githubusercontent.com/google/material-design-icons/master/sprites/svg-sprite/svg-sprite-action.svg', 24)
    .iconSet('alert', 'https://raw.githubusercontent.com/google/material-design-icons/master/sprites/svg-sprite/svg-sprite-alert.svg', 24)
    .iconSet('av', 'https://raw.githubusercontent.com/google/material-design-icons/master/sprites/svg-sprite/svg-sprite-av.svg', 24)
    .iconSet('communication', 'https://raw.githubusercontent.com/google/material-design-icons/master/sprites/svg-sprite/svg-sprite-communication.svg', 24)
    .iconSet('content', 'https://raw.githubusercontent.com/google/material-design-icons/master/sprites/svg-sprite/svg-sprite-content.svg', 24)
    .iconSet('device', 'https://raw.githubusercontent.com/google/material-design-icons/master/sprites/svg-sprite/svg-sprite-device.svg', 24)
    .iconSet('editor', 'https://raw.githubusercontent.com/google/material-design-icons/master/sprites/svg-sprite/svg-sprite-editor.svg', 24)
    .iconSet('file', 'https://raw.githubusercontent.com/google/material-design-icons/master/sprites/svg-sprite/svg-sprite-file.svg', 24)
    .iconSet('hardware', 'https://raw.githubusercontent.com/google/material-design-icons/master/sprites/svg-sprite/svg-sprite-hardware.svg', 24)
    .iconSet('image', 'https://raw.githubusercontent.com/google/material-design-icons/master/sprites/svg-sprite/svg-sprite-image.svg', 24)
    .iconSet('maps', 'https://raw.githubusercontent.com/google/material-design-icons/master/sprites/svg-sprite/svg-sprite-maps.svg', 24)
    .iconSet('navigation', 'https://raw.githubusercontent.com/google/material-design-icons/master/sprites/svg-sprite/svg-sprite-navigation.svg', 24)
    .iconSet('notification', 'https://raw.githubusercontent.com/google/material-design-icons/master/sprites/svg-sprite/svg-sprite-notification.svg', 24)
    .iconSet('social', 'https://raw.githubusercontent.com/google/material-design-icons/master/sprites/svg-sprite/svg-sprite-social.svg', 24)
    .iconSet('toggle', 'https://raw.githubusercontent.com/google/material-design-icons/master/sprites/svg-sprite/svg-sprite-toggle.svg', 24)

  // Illustrated user icons used in the docs https://material.angularjs.org/latest/#/demo/material.components.gridList
  .iconSet('avatars', 'https://raw.githubusercontent.com/angular/material/master/docs/app/icons/avatar-icons.svg', 24)
    .defaultIconSet('https://raw.githubusercontent.com/google/material-design-icons/master/sprites/svg-sprite/svg-sprite-action.svg', 24);
});
app.controller('AppCtrl', ['$scope', '$mdBottomSheet', '$mdSidenav', '$mdDialog', '$http', function($scope, $mdBottomSheet, $mdSidenav, $mdDialog, $http) {
  /**
   * List of colors for the flash cards
   * @type {Array}
   */
  $scope.colors = ['red', 'blue', 'green', 'darkBlue', 'yellow', 'purple', 'deepBlue', 'lightPurple'];

  $scope.fetchFlashCards = function(keyword) {
    var flashCards = [];
    var requestURL = BASE_URL + "category=" + keyword;
    $http.get(requestURL, {})
      .success(function (data, status, headers, config) {
        var i = 0;
        angular.forEach(data, function(flashCard) {
          flashCard.fcid = i++;
          flashCards.push({
            question: flashCard.term || $scope.keyword,
            answer: flashCard.definition || "./" + flashCard.term_image,
            topic: "Math",
            color: $scope.colors[flashCard.fcid % 7],
            id: flashCard.fcid
          })
        });
        $scope.flashCards = flashCards;
        $scope.$apply();
        setTimeout(function() {
          $scope.processFlashCards();
        }, 500);
      })
      .error(function(data, status) {
        $scope.messages = data || "Request failed";
        $scope.status = status;
       });

    /*$scope.flashCards = [{
      question: "What is an outlier ?",
      answer: "A number that is a lot smaller or larger than the rest",
      topic: "Algebra",
      color: "yellow",
      id: "1"
    }, {
      question: "Biased ?",
      answer: "Data that is not random and influenced by something",
      topic: "Probability",
      color: "green",
      id: "2"
    }, {
      question: "Causal Relationship",
      answer: "One event makes the other happen",
      topic: "Algebra",
      color: "pink",
      id: "3"
    }, {
      question: "Correlation",
      answer: "Two events occur at the same time, one does not cause the other",
      topic: "Algebra",
      color: "red",
      id: "4"
    }, {
      question: "Mode",
      answer: "The number that occurs the most often",
      topic: "Statistics",
      color: "blue",
      id: "5"
    }];*/
  }

  $scope.processFlashCards = function() {
    var cardsDom = document.getElementsByClassName("flashCard");
    angular.forEach(cardsDom, function(cardDom) {
      var cardInnerDom = cardDom.children[0].children[2];
      var cardInnerHtml = cardInnerDom.children[0].innerHTML.trim();
      if (cardInnerHtml.indexOf("./data/images") == 0) {
        cardInnerDom.children[0].innerHTML = "";
        angular.element(cardInnerDom).css("background-repeat", 'no-repeat');
        angular.element(cardInnerDom).css("background-position", 'center');
        angular.element(cardInnerDom).css("background-image", 'url("' + cardInnerHtml + '")');
      }
    })
  }

  // Toolbar search toggle
  $scope.toggleSearch = function(element) {
    $scope.showSearch = !$scope.showSearch;
  };

  // Sidenav toggle
  $scope.toggleSidenav = function(menuId) {
    $mdSidenav(menuId).toggle();
  };

  $scope.toggleFlashCard = function($event) {
    var card = $event.currentTarget;
    if (card && card.id) {
      var cardDom = angular.element(card);
      if (cardDom.hasClass("closedCard")) {
        cardDom.removeClass("closedCard");
        cardDom.addClass("openedCard");
      } else {
        cardDom.removeClass("openedCard");
        cardDom.addClass("closedCard");
      }
    }
  }

  // Menu items
  $scope.menu = [{
    link: '',
    title: 'Cardboard',
    icon: 'action:ic_dashboard_24px' // we have to use Google's naming convention for the IDs of the SVGs in the spritesheet
  }, {
    link: '',
    title: 'Friends',
    icon: 'social:ic_group_24px'
  }];
  $scope.admin = [{
    link: '',
    title: 'Trash',
    icon: 'action:ic_delete_24px'
  }, {
    link: 'showListBottomSheet($event)',
    title: 'Settings',
    icon: 'action:ic_settings_24px'
  }];


  // Bottomsheet & Modal Dialogs
  $scope.alert = '';
  $scope.showListBottomSheet = function($event) {
    $scope.alert = '';
    $mdBottomSheet.show({
      template: '<md-bottom-sheet class="md-list md-has-header"><md-list><md-list-item class="md-2-line" ng-repeat="item in items" role="link" md-ink-ripple><md-icon md-svg-icon="{{item.icon}}" aria-label="{{item.name}}"></md-icon><div class="md-list-item-text"><h3>{{item.name}}</h3></div></md-list-item> </md-list></md-bottom-sheet>',
      controller: 'ListBottomSheetCtrl',
      targetEvent: $event
    }).then(function(clickedItem) {
      $scope.alert = clickedItem.name + ' clicked!';
    });
  };

  $scope.startSearch = function(ev, $http) {
    $mdDialog.show({
        controller: DialogController,
        template: '<md-dialog aria-label="Generate Flash Card" ng-cloak> <form> <md-toolbar> <div class="md-toolbar-tools"> <h2>Generate Flash Cards On</h2> <span flex></span> <md-button class="md-icon-button" ng-click="cancel()"> <md-icon md-svg-icon="navigation:ic_close_24px" aria-label="Close Dialog"></md-icon> </md-button> </div> </md-toolbar> <md-dialog-content style="max-width:800px;max-height:810px; "> <md-input-container md-theme="input" flex> <label>Fetch flash cards for</label> <input autocomplete="off" data-ng-model="keyword" placeholder="Fetch flash cards for"> </md-input-container> </md-dialog-content> <div class="md-actions" layout="row"> <md-button ng-click="answer(keyword)" style="margin-right:20px;" > Go </md-button> </div> </form> </md-dialog>',
        parent: angular.element(document.body),
        targetEvent: null,
        clickOutsideToClose: true
      })
      .then(function(keyword) {
        delete $scope.flashCards;
        var me = {
          scope: $scope,
          keyword: keyword,
          $http: $http
        };
        setTimeout(function() {
          me.scope.keyword = me.keyword;
          me.scope.fetchFlashCards(me.keyword, me.$http);
          me.scope.$apply();
        }, 500);
      }, function() {
        $scope.status = 'You cancelled the dialog.';
      });
  };
  $scope.startSearch(event, $http);
}]);

app.controller('ListBottomSheetCtrl', function($scope, $mdBottomSheet) {
  $scope.items = [{
    name: 'Share',
    icon: 'social:ic_share_24px'
  }, {
    name: 'Upload',
    icon: 'file:ic_cloud_upload_24px'
  }, {
    name: 'Copy',
    icon: 'content:ic_content_copy_24px'
  }, {
    name: 'Print this page',
    icon: 'action:ic_print_24px'
  }, ];

  $scope.listItemClick = function($index) {
    var clickedItem = $scope.items[$index];
    $mdBottomSheet.hide(clickedItem);
  };
});

function DialogController($scope, $mdDialog) {
  $scope.hide = function() {
    $mdDialog.hide();
  };
  $scope.cancel = function(answer) {
    $mdDialog.hide(answer);
  };
  $scope.answer = function(answer) {
    $mdDialog.hide(answer);
  };
};

app.config(function($mdThemingProvider) {
  var customBlueMap = $mdThemingProvider.extendPalette('light-blue', {
    'contrastDefaultColor': 'light',
    'contrastDarkColors': ['50'],
    '50': 'ffffff'
  });
  $mdThemingProvider.definePalette('customBlue', customBlueMap);
  $mdThemingProvider.theme('default')
    .primaryPalette('customBlue', {
      'default': '500',
      'hue-1': '50'
    })
    .accentPalette('pink');
  $mdThemingProvider.theme('input', 'default')
    .primaryPalette('grey')
});