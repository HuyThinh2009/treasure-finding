#include "function.cpp"

int main(){
    int n = 3;
    int arr[MAXN][MAXN];
    createMap(n,arr);
    for(int i=0;i<2*n+1;i++){
        for(int j=0;j<2*n+1;j++){
            cout<<arr[i][j]<<' ';
        }
        cout<<'\n';
    }
}