#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <stdio.h>
#include <stdlib.h>

using namespace cv;
using namespace std;

Mat GetThresholdedImage( Mat imgHSV, Scalar lower, Scalar upper ) ;
Point computeCentroid( Mat &mask ) ;

int main( int argc, char *argv[] ) {

  /* open the first camera available */
  VideoCapture cap( 0 ) ;

  if ( !cap.isOpened() )
    return -1 ;

  Mat scaled ;
  Point centroid ;

  Scalar lower = Scalar(14, 200, 60) ;
  Scalar upper = Scalar(22, 245, 220) ;

  namedWindow( "Source", CV_WINDOW_AUTOSIZE ) ;
  namedWindow( "Thresholded", CV_WINDOW_AUTOSIZE ) ;
  namedWindow( "Thresholded_Eroded", CV_WINDOW_AUTOSIZE ) ;

  while ( true ) {

    /* grab a new frame from the camera */
    Mat src ;
    cap >> src ;
    resize( src, scaled, Size(), 0.5, 0.5 ) ;

    Mat imgHSV = Mat(scaled.size(), 8, 1) ;
    Mat thresholded  = Mat(scaled.size(), 8, 1) ;

    /* convert image to HSV and blur it */
    cvtColor( scaled, imgHSV, CV_BGR2HSV );
    blur( imgHSV, imgHSV, Size( 5, 5 ) ) ;

    /* make everything that doesn't match the color of the ball black */
    thresholded = GetThresholdedImage( imgHSV, lower, upper ) ;
    centroid = computeCentroid( thresholded ) ;
    cout << "x: " << centroid.x << " y: " << centroid.y << endl ;
    /* here is the part where I communicate with the serial port somehow */

    /* draw a circle around the center point */
    circle( scaled, centroid, 5, upper, -1 ) ;

    imshow( "Source", scaled );
    imshow( "Thresholded", thresholded ) ;

    if ( waitKey(30) >= 0 ) break ;

  }

  return 0 ;

}

Mat GetThresholdedImage( Mat imgHSV, Scalar lower, Scalar upper ) {
  // create new image same size as imgHSV
  Mat imgThresh = Mat(imgHSV.size(), 8, 1) ;
  inRange( imgHSV, lower, upper, imgThresh ) ;
  return imgThresh ;
}

Point computeCentroid( Mat &mask ) {
  // use image moments to calculate centroid
  Moments m = moments(mask, true) ;
  Point center( m.m10/m.m00, m.m01/m.m00 ) ;
  return center ;
}
