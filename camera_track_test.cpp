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
  Point blue_centroid ;
  Point black_centroid ;


  Scalar upper = Scalar(50, 250, 200) ;

  /* these two sets of Scalars should be updated to the 
     markers that are placed on the blimp */

  Scalar blue_lower = Scalar(115, 150, 60) ;
  Scalar blue_upper = Scalar(125, 220, 150) ;

  Scalar black_lower = Scalar(0, 0, 0) ;
  Scalar black_upper = Scalar(0, 0, 0) ;

  namedWindow( "Source", CV_WINDOW_AUTOSIZE ) ;
  namedWindow( "Blue Thresholded", CV_WINDOW_AUTOSIZE ) ;
  namedWindow( "Black Thresholded", CV_WINDOW_AUTOSIZE ) ;
  while ( true ) {

    /* grab a new frame from the camera */
    Mat src ;
    cap >> src ;
    resize( src, scaled, Size(), 0.5, 0.5 ) ;

    Mat imgHSV = Mat(scaled.size(), 8, 1) ;
    Mat blue_thresholded  = Mat(scaled.size(), 8, 1) ;
    Mat black_thresholded = Mat(scaled.size(), 8, 1) ;

    /* convert image to HSV and blur it */
    cvtColor( scaled, imgHSV, CV_BGR2HSV );
    blur( imgHSV, imgHSV, Size( 5, 5 ) ) ;

    /* create some binary images */
    blue_thresholded = GetThresholdedImage( imgHSV, blue_lower, blue_upper ) ;
    black_thresholded = GetThresholdedImage( imgHSV, black_lower, black_upper ) ;
    blue_centroid = computeCentroid( blue_thresholded ) ;
    black_centroid = computeCentroid( black_thresholded ) ;

    cout << blue_centroid.x << " " << blue_centroid.y << endl ;

    /* draw a circle around the center point */
    circle( scaled, blue_centroid, 5, upper, -1 ) ;
    circle( scaled, black_centroid, 5, upper, -1 ) ;

    imshow( "Source", scaled );
    imshow( "Blue Thresholded", blue_thresholded ) ;
    imshow( "Black Thresholded", black_thresholded ) ;

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
