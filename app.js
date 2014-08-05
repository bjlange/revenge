(function(){
    var app = angular.module('revenge',[ ]);
    app.controller('QBController', function(){
        this.players = qbs;
    });
    app.controller('DraftController', function(){
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

    })

    var qbs = [{name: 'Peyton Manning',
                adp: 7.4,
                tier: 1,
                proj: .39,
                drafted: false},
               {name: 'Drew Brees',
                adp: 26.3,
                tier: 1,
                proj: .88,
                drafted: false}]

})();
