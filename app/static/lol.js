// lol.js

// Flips between ascending and descending sort
function sortOrder(oldSortType, newSortType, reverse) {
  if (oldSortType == newSortType) {
    return !reverse;
  }
  else {
    return false;
  }
}

function getNumber(num) {
  var arr = new Array(num);
  for (i = 0; i < num; i++)
  {
    arr[i] = i;
  }
  return arr;
}

var lol_app = angular.module('lol_app', []);

lol_app.controller('lol_controller', function($scope, $http, $sce) {

  $scope.rut = "Unit test complete.";
  $scope.fillrut = "";

  // SUMMONERS
  //
  //

  $scope.summs_sortType     = 'name'; // set the default sort type
  $scope.summs_sortReverse  = false;  // set the default sort order
  $scope.summs_search   = '';     // set the default search/filter term

  $scope.sortOrder = sortOrder;
  $scope.getNumber = getNumber;

  // Summoners Data

  $scope.request_summoners = function() {
    $http.get("/api/summoners")
    .then(function(response) {
      $scope.summoners = response.data.summoners;
      $scope.data_loading = false;
    });
  }

  $scope.request_summoner = function (id) {
    $http.get("/api/summoner/" + id)
    .then(function(response) {
      var summoner = response.data;
      summoner.icon_url = $scope.champion_icon_url(summoner.top_3_champs[0].name);
      $scope.summoner = summoner;
      $scope.data_loading = false;
    });
  }

  function get_summoner_link(index) {
    if (index < 0 || index >= $scope.summoners.length) {
      return '#';
    }
    else {
      return '/summoner/' + index;
    }
  }

    function get_summoner_name(index) {
    if (index < 0 || index >= $scope.summoners.length) {
      return 'Not listed';
    }
    else {
      return $scope.summoners[index].name;
    }
  }

  function get_summoner_index(id) {
    for (i = 0; i < $scope.summoners.length; i++) {
      if (id == $scope.summoners[i].id) {
        return i;
      }
    }
    return -1;
  }

  $scope.get_summoner_link = get_summoner_link;
  $scope.get_summoner_name = get_summoner_name;
  $scope.get_summoner_index = get_summoner_index;

  // CHAMPIONS
  //
  //

  $scope.champs_sortType     = 'name'; // set the default sort type
  $scope.champs_sortReverse  = false;  // set the default sort order
  $scope.champs_search   = '';     // set the default search/filter term

  // Champions Data

  $scope.champion_icon_url = function(name) {
  return "http://ddragon.leagueoflegends.com/cdn/6.7.1/img/champion/" + 
    name.replace(/'(.)/, function(v) { return v.toLowerCase(); })
    .replace(/[^a-zA-Z0-9]/g,'') + ".png";
  }

  $scope.request_champs = function() {
    $http.get("/api/champions")
    .then(function(response) {
      $scope.champs = response.data.champions;
      $scope.data_loading = false;
    });
  }

  $scope.request_champ = function (id) {
    $http.get("/api/champion/" + id)
    .then(function(response) {
      var champ = response.data;
      champ.icon_url = $scope.champion_icon_url(champ.name);      
      $scope.champ = champ;
      $scope.data_loading = false;
    });
  }

  function get_champion_link(index) {
    if (index < 0 || index >= $scope.champs.length) {
      return '#';
    }
    else {
      return '/champion/' + index;
    }
  }

    function get_champion_name(index) {
    if (index < 0 || index >= $scope.champs.length) {
      return 'Not listed';
    }
    else {
      return $scope.champs[index].name;
    }
  }

  function get_champion_index(id) {
    for (i = 0; i < $scope.champs.length; i++) {
      if (id == $scope.champs[i].id) {
        return i;
      }
    }
    return -1;
  }

  $scope.get_champion_link = get_champion_link;
  $scope.get_champion_name = get_champion_name;
  $scope.get_champion_index = get_champion_index;

  // TEAMS
  //
  //

  $scope.teams_sortType     = 'name'; // set the default sort type
  $scope.teams_sortReverse  = false;  // set the default sort order
  $scope.teams_search   = '';     // set the default search/filter term

  // Teams Data

  $scope.request_teams = function() {
    $http.get("/api/teams")
    .then(function(response) {
      $scope.teams = response.data.teams;
      $scope.data_loading = false;
    });
  }

  $scope.request_team = function (id) {
    $http.get("/api/team/" + id)
    .then(function(response) {
      $scope.team = response.data;
      $scope.data_loading = false;
    });
  }

  $scope.request_search = function(query) {
    $scope.search_query = query;
    $http.get("/api/search/" + query)
    .then(function(response) {
      $scope.search_results = response.data.results;
      $scope.data_loading = false;
    });
  }

  $scope.highlight = function(text, query) {
    query = query.toLowerCase();
    var words = query.split(" ");
    for (var i = 0; i < words.length; i++) {
      if (text.toLowerCase().indexOf(words[i]) != -1) {
        var start_text = text.substring(0, text.indexOf(":") + 2);
        text = text.substring(text.indexOf(":") + 2);
        var matchIndex = text.toLowerCase().indexOf(words[i]);
        var result = start_text + text.substring(0, matchIndex) +
                                "<span class='highlight'>" + 
                                text.substring(matchIndex, matchIndex + words[i].length) + 
                                "</span>" + text.substring(matchIndex + words[i].length);
        break;
      }
    }

    return $sce.trustAsHtml(result);
  }

  $scope.data_loading = true;
});
