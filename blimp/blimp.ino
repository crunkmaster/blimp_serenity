//Rev 2 includes tests for motors and xbee communication, partly working

/*
  Required connections between Arduino and qik 2s9v1:

  Arduino   qik 2s9v1
  -------------------------
  5V - VCC
  GND - GND
  Digital Pin 2 - TX
  Digital Pin 3 - RX
  Digital Pin 4 - RESET
*/

#include <SoftwareSerial.h>
#include <PololuQik.h>
#include <Servo.h>
Servo serv;

PololuQik2s9v1 qik(2, 3, 4);

const double pi = 4 * atan( (float)1 ) ;
const double sigma = 0.3 ;

double phi, phi_r ;
double turning_angle ;
int x_r, y_r ;
int x, y ;
int ro;
int mu = 10;

void setup() {

    Serial.begin( 9600 ) ;

    qik.init();
    serv.attach(6);
    serv.write(90);

    stop();

}

void loop() {
    x_r = 0 ;
    y_r = 100 ;
    
    get_coordinates( &x, &y, &phi ) ;
    Serial.println(phi);
    phi_r = get_reference_angle( y_r, x_r, y, x ) ;
    turning_angle = get_turning_angle( phi, phi_r ) ;


    if ( turning_angle > sigma ) {
        left(get_motor_speed(turning_angle));
    }

    else{
        left(0);
        ro = sqrt( pow(y_r-y, 2) + pow(x_r - x, 2) );

        if( ro < mu ){
            stop();
        }
        else{
            forward(100);
        }
    }


    delay(10);
}

void get_coordinates( int *x, int *y, double *phi ) {

    if ( Serial.available() > 0 )
	if ( Serial.findUntil( "-", "-" )) {
	    *x = Serial.parseInt() ;
	    *y = Serial.parseInt() ;
	    *phi = (Serial.parseInt() / (float)10000);
	}
}

double get_reference_angle( int y_r, int x_r, int y, int x )  {
    double intermediate ;
    double phi_r ;

    intermediate = atan2( y_r - y, x_r - x ) ;

    // Change -pi to pi range of atan2 to 0 to 2pi of camera coordinates
    if ( (intermediate >= 0) && (intermediate < pi) )
        phi_r = 2 * pi - intermediate ;

    if ( (intermediate > -pi) && (intermediate < 0) )
        phi_r = -intermediate;

    return phi_r ;

}

double get_turning_angle( double phi, double phi_r ) {
    return abs( phi - phi_r ) ;
}

void forward(int motor_speed) {
    qik.setM1Speed(motor_speed/2);
}

void reverse(int motor_speed) {
    qik.setM1Speed(-motor_speed/2);
}

void left(int motor_speed) {
    qik.setM0Speed(-motor_speed/2);
}

void right(int motor_speed) {
    qik.setM0Speed(motor_speed/2);
}

void stop() {
    qik.setM1Speed(0);
    qik.setM0Speed(0);

}

int get_motor_speed( double turning_angle)
{
    int motor_speed;
    if( turning_angle < 3 * sigma) {
        motor_speed = turning_angle * 40;
    }
    else{
        motor_speed = 254;
    }

    return motor_speed;
}
