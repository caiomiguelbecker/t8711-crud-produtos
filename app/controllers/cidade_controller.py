import os
from app.models.cidade import Cidade


class Cidade_Controller:

    def __init__(self, dao, estado_dao, view):
        self.dao = dao
        self.estado_dao = estado_dao
        self.view = view
        self.cidade_selecionado = None

    def new(self):
        self.view.limpar_campos()
        self.cidade_selecionado = None

    def carregar_estados(self):
        estados = self.estado_dao.get_all()
        self.view.carregar_estados(estados)

    def save(self):

        try:

            nome, estado = self.view.ler_dados_cidade()

            cidade = Cidade(
                None,
                nome,
                estado
            )

            self.dao.save(cidade)

            self.get_all()

            self.view.exibir_mensagem(
                "Cidade cadastrada com sucesso!"
            )

        except ValueError as e:

            self.view.exibir_mensagem(
                f"Erro: {str(e)}",
                False
            )

    def get_all(self):

        cidades = self.dao.get_all()

        self.view.exibir_cidades(
            cidades
        )

    def selecionar_cidade(self, event):

        try:

            id_cidade = self.view.get_id_selecionado()

            if id_cidade is None:
                return

            self.cidade_selecionado = self.dao.get_by_id(
                id_cidade
            )

            self.view.preencher_campos(
                self.cidade_selecionado
            )

        except Exception:
            pass

    def update(self):

        try:

            if self.cidade_selecionado is None:

                self.view.exibir_mensagem(
                    "Selecione uma cidade na lista.",
                    False
                )

                return

            nome, estado = self.view.ler_dados_cidade()

            self.cidade_selecionado.atualizar_dados(
                nome,
                estado
            )

            self.dao.update(
                self.cidade_selecionado
            )

            self.get_all()

            self.view.exibir_mensagem(
                "Cidade atualizada com sucesso!"
            )

        except ValueError as e:

            self.view.exibir_mensagem(
                f"Erro: {str(e)}",
                False
            )

    def delete(self):

        if self.cidade_selecionado is None:

            self.view.exibir_mensagem(
                "Selecione uma cidade na lista.",
                False
            )

            return

        if not self.view.confirmar_exclusao():
            return

        try:

            sucesso = self.dao.delete(
                self.cidade_selecionado.id
            )

            if sucesso:

                self.cidade_selecionado = None

                self.view.limpar_campos()

                self.get_all()

                self.view.exibir_mensagem(
                    "Cidade excluída com sucesso!"
                )

            else:

                self.view.exibir_mensagem(
                    "Cidade não encontrada.",
                    False
                )

        except Exception as e:

            self.view.exibir_mensagem(
                f"Erro: {str(e)}",
                False
            )

    def inicializar_sistema(self):

        while True:

            os.system(
                'cls' if os.name == 'nt' else 'clear'
            )

            opcao = self.view.renderizar_menu()

            if opcao == 0:
                break

            elif opcao == 1:
                self.save()

            elif opcao == 2:
                self.get_all()

            elif opcao == 3:
                self.update()

            elif opcao == 4:
                self.delete()

            else:

                self.view.exibir_mensagem(
                    "Opção inválida. Tente novamente.",
                    False
                )