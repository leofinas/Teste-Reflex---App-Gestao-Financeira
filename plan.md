# Plano de Desenvolvimento - App de Gestão Financeira Pessoal

## Objetivo
Criar uma aplicação web que permita cadastrar ganhos mensais, despesas fixas mensais e anuais, e compras parceladas, exibindo um gráfico de pizza com a distribuição dos gastos.

---

## Phase 1: Formulários de Entrada e Gerenciamento de Estado ✅
- [x] Criar estrutura de estado para armazenar ganhos mensais recorrentes (salário, dividendos)
- [x] Implementar formulário para cadastro de despesas mensais fixas (água, luz, IPTU, aluguel)
- [x] Implementar formulário para cadastro de despesas anuais fixas (IPVA, assinaturas)
- [x] Implementar formulário para cadastro de compras parceladas (valor total, parcelas)
- [x] Adicionar funcionalidade de adicionar, editar e remover itens de cada categoria

---

## Phase 2: Visualização com Gráfico de Pizza e Dashboard ✅
- [x] Calcular total mensal de gastos (incluindo despesas mensais + anuais/12 + parcelas mensais)
- [x] Implementar gráfico de pizza usando recharts mostrando distribuição de gastos por categoria
- [x] Criar resumo financeiro com receitas totais vs despesas totais
- [x] Adicionar indicador de saldo mensal (receitas - despesas)
- [x] Exibir lista detalhada de todas as despesas cadastradas

---

## Phase 3: Layout e Melhorias de UI/UX ✅
- [x] Criar layout responsivo com navegação entre seções
- [x] Adicionar validação de formulários e mensagens de feedback
- [x] Implementar design com cores e estilos consistentes
- [x] Adicionar ícones e melhorias visuais nos cards e formulários
- [x] Garantir que todos os textos e labels estejam em português

---

## Phase 4: UI Verification ✅
- [x] Testar formulário de renda com valores válidos e verificar toast de confirmação
- [x] Testar formulário de despesas mensais e parcelamento com múltiplos itens
- [x] Verificar gráfico de pizza renderiza corretamente com dados preenchados
- [x] Validar que o layout responsivo funciona e todos os elementos estão visíveis

---

## Phase 5: Sistema de Autenticação com Google ✅
- [x] Configurar Google OAuth com credenciais do ambiente
- [x] Implementar página de login com botão "Sign in with Google"
- [x] Proteger toda a aplicação com autenticação obrigatória
- [x] Adicionar header com informações do usuário (nome, email, avatar)
- [x] Implementar botão de logout funcional
- [x] Testar fluxo completo de autenticação

---

## Phase 6: Persistência de Dados com MongoDB ✅
- [x] Criar módulo de conexão MongoDB (app/database.py)
- [x] Configurar conexão singleton com MongoDB Atlas usando MONGODB_URI
- [x] Implementar função `load_data()` para carregar dados do usuário ao fazer login
- [x] Modificar todos os eventos (add/remove) para salvar automaticamente no MongoDB
- [x] Usar email do usuário (Google Auth) como identificador único
- [x] Implementar operação upsert (replace_one com upsert=True) para salvar dados
- [x] Adicionar tratamento de erros robusto com logging e fallback gracioso
- [x] Garantir que dados persistem entre sessões de login
- [x] Testar eventos de adicionar e remover com persistência automática

---

## Phase 7: UI Verification Final ✅
- [x] Testar fluxo completo: login → adicionar dados → logout → login novamente
- [x] Verificar que dados persistem corretamente entre sessões
- [x] Testar todas as operações CRUD com persistência em tempo real
- [x] Validar que mensagens de erro/sucesso são exibidas apropriadamente

---

## Phase 8: Criptografia de Dados Sensíveis ✅
- [x] Instalar biblioteca cryptography para criptografia Fernet
- [x] Criar módulo de criptografia (app/encryption.py) com geração/carregamento de chave
- [x] Implementar funções para criptografar e descriptografar valores numéricos
- [x] Modificar _save_data() para criptografar valores de amount antes de salvar
- [x] Modificar load_data() para descriptografar valores ao carregar do MongoDB
- [x] Adicionar variável de ambiente ENCRYPTION_KEY para a chave de criptografia
- [x] Implementar fallback para gerar chave automaticamente se não existir
- [x] Testar que dados são salvos criptografados e carregados corretamente

---

## Phase 9: UI Verification - Criptografia ✅
- [x] Adicionar dados financeiros e verificar que são salvos
- [x] Verificar no MongoDB que valores amount estão criptografados (não em plaintext)
- [x] Testar logout e login novamente para validar descriptografia funciona
- [x] Confirmar que todos os cálculos e visualizações continuam funcionando corretamente

---

## Phase 10: Campo Categoria para Despesas ✅
- [x] Atualizar TypedDict ExpenseItem e InstallmentItem para incluir campo "category"
- [x] Adicionar componente select com 8 categorias (Moradia, Transporte, Alimentação, Saúde, Educação, Lazer, Despesas pessoais, Outros)
- [x] Atualizar formulários de despesas mensais, anuais e parcelamentos com campo categoria obrigatório
- [x] Modificar funções add_monthly_expense, add_annual_expense, add_installment para salvar categoria
- [x] Atualizar visualização das listas para exibir a categoria de cada despesa
- [x] Atualizar funções de criptografia/descriptografia para incluir categoria
- [x] Garantir que categoria é persistida corretamente no MongoDB

---

## Phase 11: UI Verification - Categorias ✅
- [x] Testar adição de despesas mensais com diferentes categorias e verificar badges aparecem corretamente
- [x] Testar adição de despesas anuais com diferentes categorias e validar cores dos badges
- [x] Testar adição de parcelamentos com diferentes categorias
- [x] Verificar que categorias persistem após logout/login e que os dados carregam corretamente do MongoDB

---

## Phase 12: Porcentagem na Legenda do Gráfico ✅
- [x] Adicionar computed var para calcular porcentagem de cada categoria em relação ao total
- [x] Atualizar componente `pie_chart_legend_item` para exibir porcentagem ao lado do valor
- [x] Formatar exibição: "R$ 500,00 (25%)" ou layout similar
- [x] Garantir que porcentagens somam 100% corretamente

---

## Phase 13: Toggle de Privacidade para Valores ✅
- [x] Adicionar state var `hide_values: bool = True` (padrão oculto)
- [x] Criar botão toggle no header para alternar visibilidade dos valores
- [x] Implementar lógica com rx.cond que retorna "****" quando hide_values=True
- [x] Aplicar mascaramento em: cards de resumo, listas de itens, totais na legenda
- [x] Garantir que porcentagens SEMPRE ficam visíveis (não são ocultadas)
- [x] Manter gráfico de pizza sempre visível (apenas valores numéricos são ocultados)

---

## Phase 14: Funcionalidade de Edição de Itens ✅
- [x] Adicionar state vars para controlar edição: `editing_item_type`, `editing_item_index`, `editing_item_data`, `is_editing`
- [x] Criar botão "Editar" em cada item das listas (income, monthly_expense, annual_expense, installment)
- [x] Implementar modal de edição com formulário preenchido com dados atuais
- [x] Criar eventos `start_edit_income`, `start_edit_monthly_expense`, `start_edit_annual_expense`, `start_edit_installment`
- [x] Implementar eventos `save_edit` e `cancel_edit` para confirmar/cancelar edição
- [x] Atualizar item no state e chamar _save_data() após edição bem-sucedida
- [x] Adicionar validação de campos durante edição

---

## Phase 15: UI Verification - Novas Funcionalidades ✅
- [x] Testar exibição de porcentagens na legenda do gráfico com dados reais
- [x] Testar toggle de privacidade (clicar no botão de olho e verificar valores ocultos/visíveis)
- [x] Validar que porcentagens permanecem visíveis mesmo com valores ocultos
- [x] Testar edição de itens de cada tipo (clicar em editar, modificar campos, salvar)
- [x] Verificar que modal de edição abre e fecha corretamente
- [x] Validar que cancelar edição não altera os dados