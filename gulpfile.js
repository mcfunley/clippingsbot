var gulp = require('gulp');
var less = require('gulp-less');
var path = require('path');
var sourcemaps = require('gulp-sourcemaps');
var livereload = require('gulp-livereload');
var favicons = require('gulp-favicons');
var util = require('gulp-util');

gulp.task('images', function() {
  return gulp.src('./frontend/img/*')
    .pipe(gulp.dest('./static/img'));
});

gulp.task('favicons', function() {
  return gulp.src('./frontend/img/clippingsbot.png')
    .pipe(favicons({}))
    .on('error', util.log)
    .pipe(gulp.dest('./static/favicon'));
});

gulp.task('less', function() {
  return gulp.src('./frontend/less/*.less')
    .pipe(sourcemaps.init())
    .pipe(less())
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest('./static'));
});

gulp.task('build', ['less', 'favicons', 'images']);

gulp.task('watch', function() {
  livereload.listen();
  gulp.watch('./frontend/**', ['build']);
});
