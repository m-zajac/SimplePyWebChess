
var Pieces = Backbone.Collection.extend({
    reset_moves: function(){
        _.each(this.models, function(m){
            m.set('moves', []);
        });
    }
});

var Piece = Backbone.Model.extend({
    image_prefix: '/chess/static/img',
    image_ext: 'png',
    image: 'Pawn',

    initialize: function(is_black) {
        this.is_black = !!is_black;
    },

    getImage: function() {
        return this.image_prefix + '/' + this.image + (this.get('is_black') ? 'B' : '') + '.' + this.image_ext;
    },

    addMove: function(move) {
        var moves = this.get('moves');
        moves.push(move);
        this.set('moves', moves);
    },

    canMoveTo: function(x, y) {
        var moves_data = this.get('moves');
        for (i in moves_data) {
            var m = moves_data[i].moves[0][1]
            if (m[0] == x && m[1] == y) {
                return true
            }
        }
        return false;
    },

    getMovePositions: function() {
        var moves_data = this.get('moves');
        if (!moves_data) {
            return [];
        }
        
        var moves = [];
        for (i in moves_data) {
            moves.push(moves_data[i].moves[0][1])
        }

        return moves;
    },

    getMoveByTarget: function(dest_array) {
        var moves_data = this.get('moves');
        if (!moves_data) {
            return null;
        }

        for (i in moves_data) {
            md = moves_data[i].moves[0][1]
            if (md[0] == dest_array[0] && md[1] == dest_array[1]) {
                return moves_data[i];
            }
        }

        return null;
    }
});

var King = Piece.extend({
    image: 'King'
});

var Queen = Piece.extend({
    image: 'Queen'
});

var Rook = Piece.extend({
    image: 'Rook'
});

var Knight = Piece.extend({
    image: 'Knight'
});

var Bishop = Piece.extend({
    image: 'Bishop'
});

var Pawn = Piece.extend({
    image: 'Pawn'
});