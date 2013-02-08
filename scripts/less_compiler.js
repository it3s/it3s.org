#! /usr/bin/env node

var exec       = require('child_process').exec,
    fs_watcher = require('./fs_watcher');

var baseDir = 'static/css/';

var formatedDate = function(date){
  return '' + date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds();
};

var compileLess = function() {
    var cmd = 'lessc static/css/style.less > static/css/style.css',
        now = new Date();

    console.log('[less] ' + formatedDate(now) + ' : style.less');
    exec(cmd, function(error, stdout, stderr){
        if (stdout) {
          console.log(stdout);
        }
        if (error !== null) {
          console.log('error:: ' + error);
        }
    });
};


fs_watcher.watch('static/css', /.*\.less$/, function(path, curr, prev){
  compileLess();
});
