require.config({
    paths: {
        molly: '/test/molly/ui/html5/assets/js/modules',
        vendors: '/test/molly/ui/html5/assets/js/vendors',
        'vendor-styles': '/test/molly/ui/html5/assets/style/vendors'
    },
    map: {
        '*': {
            'css': 'vendors/require-css'
        }
    }
});