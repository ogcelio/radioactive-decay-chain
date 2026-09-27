#include <stdio.h>
#include <stdlib.h>
#include "dados.h"

int main(int argc, char *argv[])
{
    // LENDO CONSTANTES PELA LINHA DE COMANDO
    const double DELTA_T = atof(argv[1]);

    // CONSTANTES DERIVADAS
    const int NUM_PTS = (int)(TF / DELTA_T) + 1;

    // CRIANDO VETORES DE COMPONENTES
    int size = NUM_PTS * sizeof(double);
    double* n1 = (double*)malloc(size);
    double* n2 = (double*)malloc(size);
    double* n3 = (double*)malloc(size);
    double* n4 = (double*)malloc(size);
    double* n5 = (double*)malloc(size);

    // APLICANDO CONDIÇÕES INCIAIS
    n1[0] = N1_0;
    n2[0] = 0.0;
    n3[0] = 0.0;
    n4[0] = 0.0;
    n5[0] = 0.0;

    for (int i = 0; i < NUM_PTS - 1; i++)
    {
        // ATUALIZANDO AS COMPONENTES DE W
        n1[i + 1] = n1[i] + DELTA_T * (-L1 * n1[i]);
        n2[i + 1] = n2[i] + DELTA_T * (L1 * n1[i] - L2 * n2[i]);
        n3[i + 1] = n3[i] + DELTA_T * (L2 * n2[i] - L3 * n3[i]);
        n4[i + 1] = n4[i] + DELTA_T * (L3 * n3[i] - L4 * n4[i]);
        n5[i + 1] = n5[i] + DELTA_T * (L4 * n4[i]);
    }

    // IMPRIMINDO PARAMETROS
    printf("DELTA_T %lf\n", DELTA_T);
    printf("NUM_PTS %d\n", NUM_PTS);

    // IMPRIMINDO RESULTADOS
    printf("N1 ");
    for (int i = 0; i < NUM_PTS; i++) {
        printf("%.16e ", n1[i]);
    }
    printf("\n");

    printf("N2 ");
    for (int i = 0; i < NUM_PTS; i++) {
        printf("%.16e ", n2[i]);
    }
    printf("\n");

    printf("N3 ");
    for (int i = 0; i < NUM_PTS; i++) {
        printf("%.16e ", n3[i]);
    }
    printf("\n");

    printf("N4 ");
    for (int i = 0; i < NUM_PTS; i++) {
        printf("%.16e ", n4[i]);
    }
    printf("\n");

    printf("N5 ");
    for (int i = 0; i < NUM_PTS; i++) {
        printf("%.16e ", n5[i]);
    }
    printf("\n");

    // LIBERANDO MEMORIA
    free(n1);
    free(n2);
    free(n3);
    free(n4);
    free(n5);

    return 0;
}
