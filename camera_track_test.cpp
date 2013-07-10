#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <stdio.h>
#include <stdlib.h>

using namespace cv;
using namespace std;

Mat GetThresholdedImage( Mat imgHSV, Scalar lower, Scalar upper ) ;
Point computeCentroid( Mat &mask ) ;
Mat combineImages( Mat img1, Mat img2 ) ;

int main( int argc, char *argv[] ) {

  /* open the first camera available */
  VideoCapture cap( 0 ) ;

  if ( !cap.isOpened() )
    return -1 ;

  Mat scaled ;
  Point blue_centroid ;
  Point red_centroid ;

  /* these two sets of Scalars should be updated to the 
     markers that are placed on the blimp */

  Scalar blue_lower = Scalar(115, 120, 0) ;
  Scalar blue_upper = Scalar(125, 220, 254) ;

  Scalar red_lower = Scalar(0, 150, 0) ;
  Scalar red_upper = Scalar(15, 240, 254) ;

  namedWindow( "Source", CV_WINDOW_AUTOSIZE ) ;
  // namedWindow( "Blue Thresholded", CV_WINDOW_AUTOSIZE ) ;
  // namedWindow( "Red Thresholded", CV_WINDOW_AUTOSIZE ) ;
  namedWindow( "Thresholded", CV_WINDOW_AUTOSIZE ) ;

  while ( true ) {

    /* grab a new frame from the camera */
    Mat src ;
    cap >> src ;
    resize( src, scaled, Size(), 0.5, 0.5 ) ;

    Mat imgHSV = Mat(scaled.size(), 8, 1) ;
    Mat blue_thresholded  = Mat(scaled.size(), 8, 1) ;
    Mat red_thresholded = Mat(scaled.size(), 8, 1) ;
    Mat both_thresholded = Mat(scaled.size(), 8, 1) ;

    /* convert image to HSV and blur it */
    medianBlur(scaled, scaled, 9);
    cvtColor( scaled, imgHSV, CV_BGR2HSV );

    /* create some binary images */
    blue_thresholded = GetThresholdedImage( imgHSV, blue_lower, blue_upper ) ;
    red_thresholded = GetThresholdedImage( imgHSV, red_lower, red_upper ) ;
    /* dilate the thresholded images to fill in holes */
    dilate( blue_thresholded, blue_thresholded, Mat(), Point(-1, -1));
    dilate( red_thresholded, red_thresholded, Mat(), Point(-1, -1));
    both_thresholded = combineImages( red_thresholded, blue_thresholded ) ;
    blue_centroid = computeCentroid( blue_thresholded ) ;
    red_centroid = computeCentroid( red_thresholded ) ;

    cout << blue_centroid.x << " " << blue_centroid.y << " " ;
    cout << red_centroid.x << " " << red_centroid.y << endl ;

    /* draw a circle around the center point */
    circle( scaled, blue_centroid, 5, blue_upper, -1 ) ;
    circle( scaled, red_centroid, 5, red_upper, -1 ) ;

    imshow( "Source", scaled );
    // imshow( "Blue Thresholded", blue_thresholded ) ;
    // imshow( "Red Thresholded", red_thresholded ) ;
    imshow( "Thresholded", both_thresholded ) ;

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

Mat combineImages( Mat img1, Mat img2 ) {
  int rows = img1.rows ;
  int cols = img1.cols ;
  Mat dst = cvCreateMat(rows, 2 * cols, img1.type()) ;
  Mat tmp = dst(cv::Rect(0, 0, cols, rows));
  img1.copyTo(tmp); 
  tmp = dst(cv::Rect(cols, 0, cols, rows)) ;
  img2.copyTo(tmp);
  return dst ;
}
