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
    int pre_correct =0;
    float base[6]{};                    
    for(float a = -1; a !=0 && a<=1 ; a+=0.1){
    for(float b = -1; b !=0 && b<=1 ; b+=0.1){
    for(float c = -1; c !=0 && c<=1 ; c+=0.1){
    for(float d = -1; d !=0 && d<=1 ; d+=0.1){
    for(float e = -1; e !=0 && e<=1 ; e+=0.1){
    for(float f = -1; f !=0 && f<=1 ; f+=0.1){
        int correct_count = 0;                
        for (int i = 0; i < 7; ++i) {
            float big = -10;
            int dir =0;
            for(int j =0;j<4;j++){
                float mount = (static_cast<float>(countMount[i][j]))/3.0;   
                float step = (static_cast<float>(inFront[i][j]));        
                float priority = (static_cast<float> (j+1))/4;
                float temp = 1.0/(a*(b+mount)+c*(d+step) + e*priority+f); 
                if(temp>big){
                    dir = j+1;
                    big = temp;
                }
            }
            if(dir==result[i]){
                correct_count++;
            }
        }
        if(correct_count>pre_correct){
            pre_correct = correct_count;
            base[0]=a;
            base[1]=b;
            base[2]=c;
            base[3]=d;
            base[4]=e;
            base[5]=f;
        }
    }
    }
    }
    }
    }
    }
    for(int i=0;i<6;i++){
        cout<<base[i]<<' ';
    }
    cout<<'\n'<<pre_correct;
    return 0;
}