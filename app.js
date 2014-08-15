(function(){
    var app = angular.module('revenge',["localytics.directives",'ngGrid']);
    app.controller('DraftController', function(){
        this.positions = ['QB','RB','WR','TE'];
        this.user_initial = 3;
        this.current_pick = 1;
        this.situations = {};
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
        this.pick_array = Array(8).join('ABCDEFGHIJKLLKJIHGFEDCBA');

        this.team_tallies = {};
        this.team_projected = {};
        this.setup_teams = function() {
            for(i=0;i < 12;i++){
                this.team_tallies[this.pick_array[i]] = {QB:0,
                                                         WR:0,
                                                         RB:0,
                                                         TE:0,
                                                         DEF:0,
                                                         K:0};
                this.team_projected[this.pick_array[i]] = {QB:0,
                                                           WR:0,
                                                           RB:0,
                                                           TE:0};
            }
            for(i=0; i<this.positions.length;i++){
                this.situations[this.positions[i]] = {};
            }
        }
        this.update_team_situations = function() {
            var teams_before_next_pick = this.teams_before_next_pick;
            var unique_teams = {};
            this.situations = {};
            for(var i=0; i<teams_before_next_pick.length; i++) {
                unique_teams[teams_before_next_pick[i]] = true;
            }
            for(var i=0; i<this.positions.length; i++) {
                var position =  this.positions[i];
                this.situations[position] = {}

                for(var team in unique_teams) {
                    var tally = this.team_tallies[team][position];
                    var projected = this.team_projected[team][position];
                    if(tally in this.situations[position]) {
                        this.situations[position][tally].push(team + " (" + projected + ")");
                    }
                    else {
                        this.situations[position][tally] = [team + " (" + projected + ")"];
                    }
                }
            }
        }
        this.teams_before_next_pick = [];
        this.update_teams_before_next_pick = function() {
            this.teams_before_next_pick = this.pick_array.slice(this.current_pick+1,
                                                                this.practical_next_pick()-1)};
        this.get_current_round = function() {
            return Math.floor((this.current_pick-1)/12)+1
        };

        this.get_round_pick = function() {
            var mod = this.current_pick % 12;
            if(mod === 0) {mod = 12};
            return mod;
        };

        this.submit_pick = function() {
            var ind = this.all_players.indexOf(this.player_selected);
            var projected = this.all_players[ind]['projected_pts'];
            var position = this.all_players[ind]['pos'];
            this.all_players.splice(ind, 1);
            this.team_tallies[this.pick_array[this.current_pick-1]][position] += 1;
            this.team_projected[this.pick_array[this.current_pick-1]][position] += projected;
            this.update_teams_before_next_pick();
            this.update_team_situations();
            this.current_pick += 1;
        };
        this.picking_now = function() {
            return(this.current_pick ===
                   this.round_to_pick(this.user_initial,
                                      this.get_current_round()));
        }
        this.user_nplus_pick = function(n) {
            var current_round_pick = this.round_to_pick(this.user_initial,
                                                        this.get_current_round());

            if(this.current_pick >= current_round_pick) {
                return this.round_to_pick(this.user_initial,
                                          this.get_current_round()+(n));
            }
            else {
                return this.round_to_pick(this.user_initial,
                                          this.get_current_round()+(n-1));
            }
        }
        this.practical_next_pick = function() {
            // this is like user_nplus_pick, but it covers the corner
            // cases where you're picking at the turn

            var next_pick = this.user_nplus_pick(1);
            if (next_pick === (this.current_pick+1)) {
                next_pick = this.user_nplus_pick(2)
            };
            return next_pick;
        }
        this.player_list = function(position) {
            return this.all_players.filter(function(element) {
                return element['pos'] === position && 'adp' in element;
            })
        };

        this.get_vorp = function(position) {
            var next_pick = this.practical_next_pick();
            var top_this = this.player_list(position).sort(function(a, b){
                return b['projected_pts'] - a['projected_pts'];
            });
            var top_score_now = top_this[0]['projected_pts'];
            var top_next = top_this.filter(function(element) {
                return element['adp'] > next_pick;
            })[0]['projected_pts'];

            return top_score_now - top_next;
        }
        this.is_undervalued = function(adp) {
            return (adp < this.current_pick);
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
        this.setup_teams();
    });
})();
