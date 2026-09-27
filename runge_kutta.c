#include <stdio.h>
#include <stdlib.h>
#include "dados.h"

void f(
    const double N1,
    const double N2,
    const double N3,
    const double N4,
    double* k)
{
    // ATUALIZANDO OS K
    k[0] = -L1 * N1;
    k[1] = L1 * N1 - L2 * N2;
    k[2] = L2 * N2 - L3 * N3;
    k[3] = L3 * N3 - L4 * N4;
    k[4] = L4 * N4;
}

int main(int argc, char *argv[])
{
    // LENDO CONSTANTES PELA LINHA DE COMANDO
    const double DELTA_T = atof(argv[1]);

    // CONSTANTES DERIVADAS
    const double SEXTO = DELTA_T / 6.0;
    const int NUM_PTS = (int)(TF / DELTA_T) + 1;

    // CRIANDO VETOR DE FATORES
    const double fator[3] = {0.5 * DELTA_T, 0.5 * DELTA_T, DELTA_T};

    // CRIANDO VETORES DE COMPONENTES
    int size = NUM_PTS * sizeof(double);
    double* n1 = (double*)malloc(size);
    double* n2 = (double*)malloc(size);
    double* n3 = (double*)malloc(size);
    double* n4 = (double*)malloc(size);
    double* n5 = (double*)malloc(size);

    // CRIANDO VETORES DE K
    size = 5 * sizeof(double);
    double* k1 = (double*)malloc(size);
    double* k2 = (double*)malloc(size);
    double* k3 = (double*)malloc(size);
    double* k4 = (double*)malloc(size);

    // APLICANDO CONDIÇÕES INCIAIS
    n1[0] = N1_0;
    n2[0] = 0.0;
    n3[0] = 0.0;
    n4[0] = 0.0;
    n5[0] = 0.0;

    for (int i = 0; i < NUM_PTS - 1; i++)
    {
        // ATUALIZANDO K1
        f(n1[i], n2[i], n3[i], n4[i], &k1[0]);

        // ATUALIZANDO K2
        f(
            n1[i] + fator[0] * k1[0],
            n2[i] + fator[0] * k1[1],
            n3[i] + fator[0] * k1[2],
            n4[i] + fator[0] * k1[3],
            &k2[0]
        );

        // ATUALIZANDO K3
        f(
            n1[i] + fator[1] * k2[0],
            n2[i] + fator[1] * k2[1],
            n3[i] + fator[1] * k2[2],
            n4[i] + fator[1] * k2[3],
            &k3[0]
        );

        // ATUALIZANDO K4
        f(
            n1[i] + fator[2] * k3[0],
            n2[i] + fator[2] * k3[1],
            n3[i] + fator[2] * k3[2],
            n4[i] + fator[2] * k3[3],
            &k4[0]
        );

        // ATUALIZANDO AS COMPONENTES DE W
        n1[i + 1] = n1[i] + SEXTO * (k1[0] + 2.0 * k2[0] + 2.0 * k3[0] + k4[0]);
        n2[i + 1] = n2[i] + SEXTO * (k1[1] + 2.0 * k2[1] + 2.0 * k3[1] + k4[1]);
        n3[i + 1] = n3[i] + SEXTO * (k1[2] + 2.0 * k2[2] + 2.0 * k3[2] + k4[2]);
        n4[i + 1] = n4[i] + SEXTO * (k1[3] + 2.0 * k2[3] + 2.0 * k3[3] + k4[3]);
        n5[i + 1] = n5[i] + SEXTO * (k1[4] + 2.0 * k2[4] + 2.0 * k3[4] + k4[4]);
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
    free(k1);
    free(k2);
    free(k3);
    free(k4);

    return 0;
}
