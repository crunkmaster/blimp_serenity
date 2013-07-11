stuff: blimp_track

blimp_track: blimp_track.cpp
	g++ blimp_track.cpp -o blimp_track `pkg-config --cflags --libs opencv`

camera_track: camera_track.cpp
	g++ camera_track.cpp -o camera_track `pkg-config --cflags --libs opencv`

camera_track_test: camera_track_test.cpp
	g++ camera_track_test.cpp -o camera_track_test `pkg-config --cflags --libs opencv`

clean:
	rm -f *.o
	rm -f camera_track
	rm -f camera_track_test
