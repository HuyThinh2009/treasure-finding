#include <iostream>

using namespace std;

int main() {
    int boards[10][3][3] = {
        // Board 1
        {{ 1,  0,  1},
         { 0, -1,  1},
         { 1,  1,  0}},

        // Board 2
        {{ 1,  1,  1},
         { 1, -1,  0},
         { 1,  1,  1}},

        // Board 3
        {{ 0,  1,  1},
         { 1, -1,  1},
         { 1,  0,  1}},

        // Board 4
        {{ 1,  1,  0},
         { 0, -1,  0},
         { 1,  1,  1}},

        // Board 5
        {{ 0,  0,  1},
         { 1, -1,  1},
         { 0,  1,  0}},

        // Board 6
        {{ 1,  1,  1},
         { 0, -1,  0},
         { 0,  1,  1}},

        // Board 7
        {{ 1,  0,  0},
         { 1, -1,  1},
         { 0,  1,  1}},

        // Board 8
        {{ 0,  1,  0},
         { 1, -1,  0},
         { 1,  0,  1}},

        // Board 9
        {{ 1,  1,  1},
         { 0, -1,  1},
         { 1,  1,  0}},

        // Board 10
        {{ 0,  1,  1},
         { 1, -1,  1},
         { 1,  0,  1}}
    };
    int result[10]{1,4,2,3,1,3,1,2,3,2};
    int countMount[10][4]{{2,2,2,2},{3,3,3,2},{2,2,2,2},{2,3,2,1},{1,1,1,2},{3,2,1,2},{1,2,2,2}};
    int inFront[10][4]={{0,1,0,1},{1,1,1,0},{1,0,1,1},{1,1,0,0},{0,1,1,1},{1,1,0,0},{0,1,1,1}};
    int priority[4]{1,2,3,4};
    // Print all boards
    int correct_count =0;
    for (int i = 0; i < 7; ++i) {
        float big = 0;
        int dir =0;
        for(int j =0;j<4;j++){
            float temp = 1/(countMount[i][j]+9999*inFront[i][j]+1.1*priority[j]+1);
            if(temp>big){
                dir = j+1;
                big = temp;
            }
        }
        if(dir==result[i]){
             correct_count++;
        }
    }
    cout<<correct_count;
    return 0;
}