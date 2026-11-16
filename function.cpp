#include "function.h"

int countMount(int n, int arr[][MAXN], int dir){
    int mounts =0;
    int starti{},endi{},startj{},endj{};
    pair<int,int> start[4] = {{0,0},{n+1,0},{0,0},{0,n+1}};
    pair<int,int> end[4] = {{n-1,2*n},{2*n,2*n},{2*n,n-1},{2*n,2*n}};
    for(int i=1;i<5;i++){
        if(i==dir){
            starti = start[i-1].first;
            startj = start[i-1].second;
            endi = end[i-1].first;
            endj = end[i-1].second;
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
int step_available(int n, int arr[][MAXN], int dir){
    int step =0;
    int x =n;
    int y =n;
    if(dir==1){
        while(x>-1 && arr[x][y]!=1){
            step++;
            x--;
        }
    }else if(dir ==2){
        while(x<2*n+1 && arr[x][y]!=1){
            step++;
            x++;
        }
    }else if(dir ==3){
        while(y>-1 && arr[x][y]!=1){
            step++;
            y--;
        }
    }else if(dir ==4){
        while(y<2*n+1 && arr[x][y]!=1){
            step++;
            y++;
        }
    }

    return step;
}

// Rảnh rỗi sinh nông nỗi
/*
void createPart(const int& n, int& arr[][], int map[], int pos){
    pair<int,int> start ={{n-1,n-1},{n,n},{n-1,2n},{n,n+1},{n+1,n+1},{n+1,n},{n+1,0},{n,n-1}};
    pair<int,int> end  = {{0,0},{0,n},{0,n+1},{n,2n},{2n,2n},{2n,n},{2n,n-1},{n,0}};
    bool plus{};
    if(pos==0||pos==1||pos==2||pos==7){
        plus =false;
    }else{
        plus = true;
    }
    if(plus){
        for(int i=start[pos].first;i<= end[pos].first;i++{
            for(int j= start[pos].second;j<= end[pos].second){
                if(map[pos]==0){
                    map[i][j]=0;
                }else if(map[pos]==)
            }
        })
    }

};
void createMap(int n, int& arr[][]){
    srand(time(0));
    int map[8]{};
    for(int i=0;i<8){
        if(i==0||i==2||i==4||i==6){
            map[i] = (29 + rand())%(n*n);
        }else{
            map[i] = (28 + rand())%(n);
        }
    }
    for(int i=0;i<8;i++){
    }
};
*/

void createMap(int n, int arr[][MAXN]){
    srand(time(0));
    for(int i=0;i<2*n+1;i++){
        for(int j=0;j<2*n+1;j++){
            int temp = rand()%2;
            arr[i][j]= temp;
        }
    }
    if(arr[n][n-1]==1&&arr[n][n+1]==1&&arr[n-1][n]==1&&arr[n+1][n]==1){
        int temp = rand()%4;
        if(temp==0){
            arr[n][n-1]=0;
        }else if(temp==1){
            arr[n][n+1]=0;
        }else if(temp==2){
            arr[n-1][n]=0;
        }else if(temp==3){
            arr[n+1][n]=0;
        }
    }
    arr[n][n]=-1;
}
int return_direct(float mounts[], float steps[], float base[]){
    float temp{};
    int dir{};
    for(int i=0;i<4;i++){
        float cur = base[0]*(base[1]+mounts[i])+base[2]*(base[3]+steps[i])+base[4]*(i+1)+base[5];
        if(1/cur >temp){
            temp = 1/cur;
            dir = i+1;
        }
    }
    return dir;
}