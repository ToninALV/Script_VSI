# Script_VSI
 Script for automation creation VSI

Input
	vlan - num-int
	pop - str
	host - str

1º Coletar Vlan no input e criar route-distinguesher e me retornar route-distinguesher que não esteja duplicado.

2º Criar nome da VSI com base no input "VL[vlan]-VSI-[pop]-[host]"

2º Selecionar a quantidade de Site-ID

3º Acessar equipamentos selecionados e atribuir o site ID relacionado e concluir configuração da VSI

4º Criar Vlan nos equipamentos 