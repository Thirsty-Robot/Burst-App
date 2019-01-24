new Vue({
    el: '#form-search',
    data: {
        animate: false,
        add_animate: false,
        summoner_name: '',
        region: '',
    },
    methods: {
        Validate: function() {
            if (this.summoner_name == '' || this.region == '') {
                this.animate = true;
                this.add_animate = true;
            }
        }
    }
});