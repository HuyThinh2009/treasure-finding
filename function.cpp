#include <function.h>

int countMount(int n, int& arr[][], int dir){
    int mounts =0;
    int starti{},endi{},startj{},endj{};
    pair<int,int> start[4] = {{0,0},{n+1,0},{0,0},{0,n+1}};
    pair<int,int> end[4] = {{n-1,2n},{2n,2n},{2n,n-1},{2n,2n}};
    for(int i=1;i<5;i++){
        if(i==dir){
            starti = start[i-1][0];
            startj = start[i-1][1];
            endi = end[i-1][0];
            endj = end[i-1][1];
        }
    }
    for(int i=starti;i<endi;i++){
        for(int j=startj;j<endj;j++){
            if(arr[i][j]==1){
                mounts++;
            }
        }
    }
    return mounts;
}
int step_available(int n, int& arr[][], int dir){
    int step =0;
    int x =n;
    int y =n;
    if(dir==1){
        while(arr[x][y]!=1&& x>-1){
            count++;
            x--;
        }
    }else if(dir ==2){
        while(arr[x][y]!=1&& x<2n+1){
            count++;
            x++;
        }
    }else if(dir ==3){
        while(arr[x][y]!=1&& y>-1){
            count++;
            x--;
        }
    }else if(dir ==4){
        while(arr[x][y]!=1&& y<2n+1){
            count++;
            y++;
        }
    }

    return step;
}
void createMap(int n, int& arr[][]){
    

}

int return_direct(float& mounts[], float& steps[], float& base[]){
    float temp{};
    int dir{};
    for(float i=0;i<4;i++){
        if(1/(mounts[i]*base[0]+step*base[1]+(i+1)*base[3]+base[4])>temp){
            temp = 1/(mounts[i]*base[0]+step*base[1]+(i+1)*base[3]+base[4]);
            dir = i+1;
        }
    }
}

//3x3: f() = 1/(count *(a+m) + step *(b+n) + c*dir + d)
//5x5