(function(){
    var app = angular.module('revenge',["localytics.directives",'ngGrid']);
    app.controller('DraftController', function(){
        this.positions = ['QB','RB','WR','TE'];
        this.user_initial = 3;
        this.current_pick = 1;
        this.round_to_pick = function(initial, round) {
            var pick = -1;
            if(round % 2 == 0) {
                pick = 12*round - initial + 1;
            }
            else {
                pick = (round-1)*12 + initial;
            }
            return pick;
        };
        this.get_current_round = function() {
            return Math.floor((this.current_pick-1)/12)+1
        };
        this.get_round_pick = function() {
            var mod = this.current_pick % 12;
            if(mod === 0) {mod = 12};
            return mod;
        };
        this.submit_pick = function() {
            this.current_pick += 1;
            var ind = this.all_players.indexOf(this.player_selected);
            this.all_players.splice(ind, 1);
        };
        this.picking_now = function() {
            return(this.current_pick ===
                   this.round_to_pick(this.user_initial,
                                      this.get_current_round()))
        }
        this.user_nplus_pick = function(n) {
            var current_round = this.round_to_pick(this.user_initial,
                                                   this.get_current_round());

            if(this.current_pick >= current_round) {
                return this.round_to_pick(this.user_initial,
                                                this.get_current_round()+(n));
            }
            else {
                return this.round_to_pick(this.user_initial,
                                          this.get_current_round()+(n-1));
            }
        }
        this.player_list = function(position) {
            return this.all_players.filter(function(element) {
                return element['pos'] === position && 'adp' in element;
            })
        };

        this.get_vorp = function(position) {
            var next_pick = this.user_nplus_pick(1);
            var top_this = this.player_list(position).sort(function(a, b){
                return b['projected_pts'] - a['projected_pts'];
            });
            var top_score_now = top_this[0]['projected_pts'];
            var top_next = top_this.filter(function(element) {
                return element['adp'] > next_pick;
            })[0]['projected_pts'];

            return top_score_now - top_next;
        }

        this.all_players = players;
        this.player_selected = this.all_players[0];
        this.grid_options = function(position) {
            return {
                data: this.player_list(position),
                columnDefs: [{field:'name', displayName:'Name'}],
            }
        }
        this.set_initial_draft_position = function() {
            this.user_initial = parseInt(prompt("Input your first round pick position:"));
        }
        this.set_initial_draft_position();
    });
})();
