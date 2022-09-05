#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int taille = 0;

void affiche_tab(char words[][taille], int nb_word);


int main(void)
	{  
		// Création d'un tableau de pointeur de type char, dont les dimensions sont dynamiques
		char *sentence = malloc(sizeof(char));
		int nb_word = 1;  
		
		printf( "Veuillez entrer une phrase : " );
		scanf("%[^\n]",sentence);

		//compte le nombre de mots 
		for(int i=0;i<strlen(sentence);i++)
		{		
			// Si la prochaine case contien un espace et que le cas actuel n'est pas un espace alors on incrémente
			if(sentence[i]!=' ' && sentence[i+1]==' ')
				nb_word++;
		}

		// Création d'un tableau de words de type char a deux dimensions, la première case récupère le nombre de mots, la deuxième la longeur de la phfrase (lettre + espace) grace a strlen
		char words[nb_word][strlen(sentence)];
		int i=0,j=0,k=0;
	do
	{
		if(sentence[i]!=' ')
			words[j][k++] = sentence[i];
		else
		{
			words[j++][k]='\0';
			k=0;
		}
	}while(sentence[i++]!='\0');

	//affiche le tableau par l'appel d'une fonction
		taille = strlen(sentence);
		affiche_tab(words, nb_word);
	
	//Libere la variable sentence de la memoire
	free(sentence);
	return 0;

	}



void affiche_tab(char words[][taille], int nb_word)
	{
		
		for(int i=0;i<nb_word;i++)
	{
		printf("%s\n",words[i]);
	}
	
	}















