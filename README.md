<h2>Introdução ao Projeto</h2>

<p>Este projeto tem como objetivo o desenvolvimento de um <strong>Sistema de Hotelaria</strong> utilizando o <strong>framework Django</strong>, uma ferramenta moderna e eficiente para criação de aplicações web com a linguagem Python. O sistema será responsável por gerenciar <strong>quartos</strong> e <strong>reservas</strong>, com funcionalidades específicas para dois tipos de usuários: <strong>Gerente</strong> e <strong>Atendente</strong>.</p>

<p>Para garantir um ambiente organizado e isolado, o projeto utiliza o <strong>venv</strong> (ambiente virtual do Python), permitindo a instalação das dependências sem interferir em outros projetos. Além disso, faz uso da biblioteca <strong>Pillow</strong>, essencial para lidar com imagens — como fotos de quartos — dentro do sistema.</p>

<h3>O que é Django?</h3>
<p>O <strong>Django</strong> é um framework web gratuito e de código aberto, escrito em Python, que facilita o desenvolvimento rápido e seguro de aplicações web. Ele fornece uma estrutura organizada para lidar com rotas, banco de dados, autenticação de usuários e interface administrativa, promovendo boas práticas e agilidade no desenvolvimento.</p>

<h3>O que é Pillow?</h3>
<p>O <strong>Pillow</strong> é uma biblioteca de processamento de imagens para Python. É frequentemente utilizada em projetos Django quando há necessidade de manipular imagens, como redimensionamento, compressão ou upload de fotos. No contexto deste projeto, o Pillow pode ser útil, por exemplo, para adicionar imagens aos quartos ou outros recursos visuais do sistema.</p>

<h3>O que é venv?</h3>
<p>O <code>venv</code> é um módulo do Python utilizado para criar <strong>ambientes virtuais</strong>, que são espaços isolados onde você pode instalar dependências específicas para um projeto sem afetar o restante do sistema. Isso é essencial para manter projetos organizados e evitar conflitos entre versões de bibliotecas.</p>

<h3>🔧 Passo a passo para configuração do ambiente:</h3>

<ul>
  <li><strong>Criando um ambiente virtual:</strong>
    <pre><code>python -m venv venv</code></pre>
  </li>
  <li><strong>Ativando o ambiente virtual:</strong>
    <pre><code>.\venv\Scripts\Activate.ps1</code></pre>
  </li>
  <li><strong>Instale o Django:</strong>
    <pre><code>pip install django</code></pre>
  </li>
  <li><strong>Instale o Pillow:</strong>
    <pre><code>pip install pillow</code></pre>
  </li>
  <li><strong>Para entrar na pasta do projeto para rodá-lo:</strong>
    <pre><code>cd Hotelaria</code></pre>
  </li>
  <li><strong>Para rodar o código:</strong>
    <pre><code>python manage.py runserver</code></pre>
  </li>
</ul>

<h3>Usuários do sistema:</h3>

<ul>
  <li><strong>Super user:</strong><br>
    Nome de usuário: <code>Administrador</code><br>
    Senha: <code>8k$JUv.4i3</code>
  </li>
  <li><strong>Gerente:</strong><br>
    Nome de usuário: <code>Gerente01</code><br>
    Senha: <code>5+vYe9X6</code>
  </li>
  <li><strong>Atendente:</strong><br>
    Nome de usuário: <code>Atendente01</code><br>
    Senha: <code>F}@8TlK76£y6</code>
  </li>
</ul>

<h3>Por que esses usuários foram criados?</h3>

<p>Esses usuários foram adicionados previamente ao sistema para facilitar os testes e demonstrações das funcionalidades implementadas. Cada um deles representa um tipo diferente de acesso:</p>

<ul>
  <li>O <strong>superusuário</strong> (<code>Administrador</code>) foi criado com privilégios administrativos completos e tem acesso ao painel de administração do Django. Ele pode criar, editar e excluir qualquer objeto no sistema, incluindo usuários, reservas e quartos. Esse tipo de usuário é usado principalmente para fins de gerenciamento e manutenção do sistema por parte do desenvolvedor ou administrador do sistema.</li>
  <li>O <strong>Gerente</strong> (<code>Gerente01</code>) é um usuário com acesso apenas às funcionalidades permitidas para sua função dentro do sistema, como o cadastro de quartos e atendentes, além da realização de reservas. Ele não tem acesso ao painel de administração do Django, apenas às funcionalidades implementadas na interface do sistema conforme as regras de negócio.</li>
</ul>

<p>Essa separação garante o controle de permissões e permite validar o correto funcionamento do controle de acesso baseado no tipo de usuário.</p>
