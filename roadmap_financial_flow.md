# Software de Gestão Financeira

### Backend:

- [ ]  Criar o modelo do usuário, com o núcle de armazenamento e segurança
    - [ ]  **User:** Armazena dados de autenticação (e-mail, senha com hash, nome).
    - [ ]  **Profile/Settings:** Preferências como moeda padrão (BRL, USD), idioma e data de fechamento da fatura
- [ ]  Modelo e estrutura de Contas e Ativos
    - [ ]  Account(Conta):
        - Campos: Onde o dinheiro está (Ex: Nubank, Itaú, etc), tipo (Conta Corrente, Poupança, Investimento), Saldo Inicial
    - [ ]  **CreditCard (Cartão de Crédito):**
        - Vinculado a uma conta ou independente.
            - *Campos:* Limite, Dia de vencimento, Dia de fechamento.
- [ ]  Movimentações financeiras:
    - [ ]  Category: Organiza os gastos
        - Campos: Nome (Alimentação, Lazer, Salário), ícone, cor, tipo (Receita ou Despesa).
        - [ ]  Gerenciamento de Categorias:
            - [ ]  Lógica de gerenciamento de Categorias
    - [ ]  Transaction (Transação): Organiza cada entrada ou saída
        - Campos: valor, data, recorrencia(mensal, semanal), descrição, id da categoria, id da conta, status (Efetivado ou pendente)
    - [ ]  Transfer (Transferencia): Para registrar dinheiro movendo-se entre suas próprias contas (ex: da Corrente para a Poupança).
- [ ]  Multi moeda ou cambio
- [ ]  Planejamento e Metas:
    - [ ]  Budget (Orçamento): Define limite de gastos por categoria
        - Id da categoria, valor limite, Mês/Ano
    - [ ]  Goal (Metas): Para objetivos especificos (Ex: Férias 2026)
        - Campos: valor objetivo, valor atual, data final
- [ ]  Relatórios e Analytics
    - Sistema para gerar relatórios de gastos por período, categoria, comparativos mês a mês, gráfico de evolução patrimonial =
- [ ]  **Notificações**
    - Sistema para alertar sobre vencimentos de contas, faturas de cartão, metas próximas do prazo, orçamentos excedidos
- [ ]  Sistema para recorrencias
    - Sistema mais robusto para gerenciar transações recorrentes (possibilidade de editar uma ocorrência ou todas, pular meses, etc.)
- [ ]  Importação de dados
    - Funcionalidade para importar extratos bancários (OFX, CSV)
- [ ]  **Compartilhamento**
    - Se for multi-usuário, sistema para compartilhar contas/orçamentos entre membros da família
- [ ]  **Auditoria/Logs**
    - Histórico de alterações para rastreabilidade
- [ ]  **Backup/Exportação**
    - Sistema para exportar todos os dados do usuário

### Frontend:

- [ ]  Criar o template do front-end
- [ ]  Página de login/cadastro
    - [ ]  Estruturar o visual
    - [ ]  Estruturar o funcional
- [ ]  Dashboard
    - [ ]  Gráfico e Visualizações (Gráfico de pizza, linha barras) para análise visual
- [ ]  Relatórios
    - Telas para visualizar relatórios mensais, anuais, por categoria
- [ ]  Gerenciamento de Categorias:
    - [ ]  Iterface para criar/editar/deletar categorias personalizadas
- [ ]  Fatura do cartão
    - Tela especifica para visualizar fatura fechada e aberta
- [ ]  Calendário financeiro
    - Visualização de transações futuras e passadas em formato de calendário
- [ ]  **Projeção de Fluxo de Caixa**:
    - Visualização gráfica do saldo projetado nos próximos meses
- [ ]  Tela de estrato detalhado
- [ ]  Filtros de data
- [ ]  Toggle para esconder valores sensíveis(”olhinho” para ocutar saldo)
- [ ]  Interface de Configurações
    - Tela para editar perfil, preferencias, segurança (trocar senha)
- [ ]  Notificações no App
    - Sistema de alertas visuais
- [ ]  Buscador Global
    - Barra de busca para encontrar rapidamente contas, transações, categorias
- [ ]  Responsividade mobile

<aside>
💡

Futuras adições

- **Parcelamento**: Sistema para gerenciar compras parceladas no cartão de crédito (crucial no Brasil!) - registrar parcela atual, total de parcelas, valor por parcela
- **Investimentos**: Módulo para controlar investimentos (ações, fundos, Tesouro Direto, CDB) com rentabilidade e atualização de valores
- **Dívidas/Empréstimos**: Controle de empréstimos, financiamentos com juros, parcelas e amortização
- **Conciliação Bancária**: Sistema para comparar o saldo registrado vs saldo real e identificar diferenças
- **Tags**: Sistema de tags flexível além de categorias (ex: uma transação pode ser "Alimentação" + "Trabalho" + "Reembolsável")
- **Anexos/Comprovantes**: Upload e armazenamento de notas fiscais, recibos vinculados às transações
- **Busca/Filtros Avançados**: Sistema robusto de busca e filtros para encontrar transações específicas
- **Projeção de Saldo**: Cálculo de saldo futuro considerando receitas/despesas programadas
- **API/Webhooks**: Para integrações com outros sistemas ou automações
- **Tema Claro/Escuro**: Alternância entre modos de visualização
- **Onboarding**: Tutorial inicial para novos usuários
- Segurança:
    - **Autenticação 2FA**: Autenticação de dois fatores
    - **Recuperação de Senha**: Sistema de reset de senha por email
    - **Sessões**: Gerenciamento de sessões ativas e logout remoto
</aside>