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

    VideoCapture cap(0) ; //attempt to open the second camera

    if ( !cap.isOpened() )
	return -1 ;

    Mat scaled ;
    int upperHue = 23 ;
    int lowerHue = 20 ;

    Point centroid ;

    Scalar lower = Scalar(lowerHue, 0, 0) ;
    Scalar upper = Scalar(upperHue, 222, 256) ;

    namedWindow( "Source", CV_WINDOW_AUTOSIZE );
    namedWindow( "Thresholded", CV_WINDOW_AUTOSIZE ) ;

    while ( true ) {

	// get a new frame from the camer
	Mat src ;
	cap >> src ;

	resize( src, scaled, Size(), 0.5, .5 ) ;

	Mat imgHSV = Mat(scaled.size(), 8, 1) ;
	Mat thresholded  = Mat(scaled.size(), 8, 1) ;

	// blur image and convert it to HSV
	cvtColor( scaled, imgHSV, CV_BGR2HSV );
	blur( scaled, scaled, Size( 5, 5 ) ) ;

	// mask out everything that doesn't match the color of the ball
	thresholded = GetThresholdedImage( imgHSV, lower, upper ) ;
	centroid = computeCentroid( thresholded ) ;
	cout << "x: " << centroid.x << " y: " << centroid.y << endl ;
	circle( scaled, centroid, 10, upper, -1 ) ;

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
    Moments m = moments(mask, true) ;
    Point center( m.m10/m.m00, m.m01/m.m00 ) ;
    return center ;
}
