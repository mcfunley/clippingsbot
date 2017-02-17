var gulp = require('gulp');
var less = require('gulp-less');
var path = require('path');
var sourcemaps = require('gulp-sourcemaps');
var livereload = require('gulp-livereload');

gulp.task('less', function() {
  return gulp.src('./frontend/less/**/*.less')
    .pipe(sourcemaps.init())
    .pipe(less({
      paths: [ path.join(__dirname, 'less', 'includes') ]
    }))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest('./static'));
});

gulp.task('build', ['less']);

gulp.task('watch', function() {
  livereload.listen();
  gulp.watch('./frontend/**', ['build']);
});
