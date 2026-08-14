-- schema.sql
-- Schema inicial do Sistema de Visitantes.
-- Deve ser executado somente em um database vazio.
-- Não contém DROP, OWNER ou GRANT específicos do ambiente.

CREATE SCHEMA IF NOT EXISTS public;

CREATE SCHEMA public AUTHORIZATION pg_database_owner;

COMMENT ON SCHEMA public IS 'standard public schema';


CREATE SEQUENCE public.autorizacao_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;




CREATE SEQUENCE public.credencial_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;




CREATE SEQUENCE public.credencial_permissao_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;




CREATE SEQUENCE public.empresa_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;




CREATE SEQUENCE public.historico_autorizacao_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;




CREATE SEQUENCE public.local_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;




CREATE SEQUENCE public.parametro_sistema_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;




CREATE SEQUENCE public.permissao_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;




CREATE SEQUENCE public.sessao_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;




CREATE SEQUENCE public.setor_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;




CREATE SEQUENCE public.status_autorizacao_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;




CREATE SEQUENCE public.tipo_usuario_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;




CREATE SEQUENCE public.usuario_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;




CREATE SEQUENCE public.veiculo_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;




CREATE SEQUENCE public.visitante_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;




CREATE SEQUENCE public.visitante_veiculo_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;


-- public.credencial definition



CREATE TABLE public.credencial (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	nome varchar(100) NOT NULL,
	ativo bool DEFAULT true NOT NULL,
	CONSTRAINT credencial_nome_key UNIQUE (nome),
	CONSTRAINT credencial_pkey PRIMARY KEY (id)
);




-- public.empresa definition



CREATE TABLE public.empresa (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	nome varchar(200) NOT NULL,
	cnpj varchar(18) NULL,
	ativo bool DEFAULT true NOT NULL,
	CONSTRAINT empresa_pkey PRIMARY KEY (id),
	CONSTRAINT empresa_unique_nome UNIQUE (nome)
);







-- public."local" definition



CREATE TABLE public."local" (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	codigo varchar(10) NOT NULL,
	descricao varchar(200) NOT NULL,
	ativo bool DEFAULT true NOT NULL,
	CONSTRAINT local_codigo_key UNIQUE (codigo),
	CONSTRAINT local_pkey PRIMARY KEY (id)
);




-- public.parametro_sistema definition



CREATE TABLE public.parametro_sistema (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	chave varchar(100) NOT NULL,
	valor varchar(500) NOT NULL,
	CONSTRAINT parametro_sistema_chave_key UNIQUE (chave),
	CONSTRAINT parametro_sistema_pkey PRIMARY KEY (id)
);




-- public.permissao definition



CREATE TABLE public.permissao (
	id serial4 NOT NULL,
	codigo varchar(100) NOT NULL,
	descricao varchar(255) NOT NULL,
	CONSTRAINT permissao_codigo_key UNIQUE (codigo),
	CONSTRAINT permissao_pkey PRIMARY KEY (id)
);




-- public.status_autorizacao definition



CREATE TABLE public.status_autorizacao (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	nome varchar(50) NOT NULL,
	descricao varchar(500) NULL,
	ativo bool DEFAULT true NOT NULL,
	participa_colisao bool DEFAULT true NOT NULL,
	CONSTRAINT status_autorizacao_nome_key UNIQUE (nome),
	CONSTRAINT status_autorizacao_pkey PRIMARY KEY (id)
);




-- public.tipo_usuario definition



CREATE TABLE public.tipo_usuario (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	nome varchar(100) NOT NULL,
	ativo bool DEFAULT true NOT NULL,
	CONSTRAINT tipo_usuario_nome_key UNIQUE (nome),
	CONSTRAINT tipo_usuario_pkey PRIMARY KEY (id)
);




-- public.veiculo definition



CREATE TABLE public.veiculo (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	placa varchar(10) NOT NULL,
	cor varchar(100) NULL,
	marca varchar(100) NULL,
	tipo varchar(100) NULL,
	observacoes varchar(1000) NULL,
	ativo bool DEFAULT true NOT NULL,
	CONSTRAINT veiculo_pkey PRIMARY KEY (id),
	CONSTRAINT veiculo_placa_key UNIQUE (placa)
);







-- public.credencial_permissao definition



CREATE TABLE public.credencial_permissao (
	id serial4 NOT NULL,
	id_credencial int4 NOT NULL,
	id_permissao int4 NOT NULL,
	CONSTRAINT credencial_permissao_pkey PRIMARY KEY (id),
	CONSTRAINT uk_credencial_permissao UNIQUE (id_credencial, id_permissao),
	CONSTRAINT fk_credencial_permissao_credencial FOREIGN KEY (id_credencial) REFERENCES public.credencial(id),
	CONSTRAINT fk_credencial_permissao_permissao FOREIGN KEY (id_permissao) REFERENCES public.permissao(id)
);




-- public.setor definition



CREATE TABLE public.setor (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	codigo varchar(10) NOT NULL,
	descricao varchar(200) NOT NULL,
	ativo bool DEFAULT true NOT NULL,
	id_local int8 NOT NULL,
	CONSTRAINT setor_codigo_key UNIQUE (codigo),
	CONSTRAINT setor_pkey PRIMARY KEY (id),
	CONSTRAINT fk_setor_local FOREIGN KEY (id_local) REFERENCES public."local"(id)
);




-- public.usuario definition



CREATE TABLE public.usuario (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	nome varchar(200) NOT NULL,
	email varchar(200) NOT NULL,
	telefone varchar(30) NULL,
	id_tipo int8 NOT NULL,
	id_setor int8 NOT NULL,
	id_credencial int8 NOT NULL,
	senha_hash varchar(255) NOT NULL,
	ativo bool DEFAULT true NOT NULL,
	data_criacao timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	data_ultima_alteracao timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	CONSTRAINT usuario_email_key UNIQUE (email),
	CONSTRAINT usuario_email_unique UNIQUE (email),
	CONSTRAINT usuario_pkey PRIMARY KEY (id),
	CONSTRAINT fk_usuario_credencial FOREIGN KEY (id_credencial) REFERENCES public.credencial(id),
	CONSTRAINT fk_usuario_setor FOREIGN KEY (id_setor) REFERENCES public.setor(id),
	CONSTRAINT fk_usuario_tipo FOREIGN KEY (id_tipo) REFERENCES public.tipo_usuario(id)
);




-- public.visitante definition



CREATE TABLE public.visitante (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	nome varchar(200) NOT NULL,
	email varchar(200) NULL,
	celular varchar(30) NULL,
	rg varchar(30) NULL,
	cpf varchar(14) NOT NULL,
	id_empresa int8 NOT NULL,
	ativo bool DEFAULT true NOT NULL,
	CONSTRAINT visitante_cpf_key UNIQUE (cpf),
	CONSTRAINT visitante_pkey PRIMARY KEY (id),
	CONSTRAINT visitante_unique_cpf UNIQUE (cpf),
	CONSTRAINT fk_visitante_empresa FOREIGN KEY (id_empresa) REFERENCES public.empresa(id)
);







-- public.visitante_veiculo definition



CREATE TABLE public.visitante_veiculo (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	id_visitante int8 NOT NULL,
	id_veiculo int8 NOT NULL,
	CONSTRAINT visitante_veiculo_pkey PRIMARY KEY (id),
	CONSTRAINT visitante_veiculo_unique UNIQUE (id_visitante, id_veiculo),
	CONSTRAINT fk_visitante_veiculo_veiculo FOREIGN KEY (id_veiculo) REFERENCES public.veiculo(id),
	CONSTRAINT fk_visitante_veiculo_visitante FOREIGN KEY (id_visitante) REFERENCES public.visitante(id)
);




-- public.autorizacao definition



CREATE TABLE public.autorizacao (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	id_visitante int8 NOT NULL,
	id_status_autorizacao int8 NOT NULL,
	primeiro_dia date NOT NULL,
	ultimo_dia date NOT NULL,
	id_setor_solicitante int8 NULL,
	id_veiculo int4 NULL,
	id_status_autorizacao_anterior int4 NULL,
	id_empresa int8 NOT NULL,
	CONSTRAINT autorizacao_pkey PRIMARY KEY (id),
	CONSTRAINT autorizacao_id_status_anterior_fkey FOREIGN KEY (id_status_autorizacao_anterior) REFERENCES public.status_autorizacao(id),
	CONSTRAINT fk_autorizacao_empresa FOREIGN KEY (id_empresa) REFERENCES public.empresa(id),
	CONSTRAINT fk_autorizacao_setor_solicitante FOREIGN KEY (id_setor_solicitante) REFERENCES public.setor(id),
	CONSTRAINT fk_autorizacao_status FOREIGN KEY (id_status_autorizacao) REFERENCES public.status_autorizacao(id),
	CONSTRAINT fk_autorizacao_veiculo FOREIGN KEY (id_veiculo) REFERENCES public.veiculo(id),
	CONSTRAINT fk_autorizacao_visitante FOREIGN KEY (id_visitante) REFERENCES public.visitante(id)
);




-- public.historico_autorizacao definition



CREATE TABLE public.historico_autorizacao (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	id_autorizacao int8 NOT NULL,
	id_usuario int8 NOT NULL,
	data_hora timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
	descricao varchar(2000) NOT NULL,
	CONSTRAINT historico_autorizacao_pkey PRIMARY KEY (id),
	CONSTRAINT fk_historico_autorizacao FOREIGN KEY (id_autorizacao) REFERENCES public.autorizacao(id),
	CONSTRAINT fk_historico_usuario FOREIGN KEY (id_usuario) REFERENCES public.usuario(id)
);




-- public.sessao definition



CREATE TABLE public.sessao (
	id int8 GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE) NOT NULL,
	id_usuario int8 NOT NULL,
	"token" varchar(500) NOT NULL,
	data_inicio timestamp NOT NULL,
	data_expiracao timestamp NOT NULL,
	CONSTRAINT sessao_pkey PRIMARY KEY (id),
	CONSTRAINT sessao_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuario(id)
);




-- public.autorizacao_consulta source

CREATE OR REPLACE VIEW public.autorizacao_consulta
AS SELECT a.id,
    a.id_visitante,
    v.nome AS visitante_nome,
    v.cpf,
    v.rg,
    v.email,
    v.celular,
    e.id AS id_empresa,
    e.nome AS empresa_nome,
    a.id_status_autorizacao_anterior,
    a.id_status_autorizacao,
    sa.nome AS status_nome,
        CASE
            WHEN a.ultimo_dia < CURRENT_DATE AND sa.nome::text = 'Autorizada'::text THEN 'Expirada'::character varying
            WHEN a.primeiro_dia > CURRENT_DATE AND sa.nome::text = 'Autorizada'::text THEN 'Pendente'::character varying
            ELSE sa.nome
        END AS status_exibicao,
    a.id_setor_solicitante,
    s.codigo AS setor_solicitante_codigo,
    s.descricao AS setor_solicitante_descricao,
    h.id_usuario,
    u.nome AS solicitante_nome,
    a.id_veiculo,
    ve.placa,
    ve.marca,
    ve.tipo,
    ve.cor,
    a.primeiro_dia,
    a.ultimo_dia
   FROM autorizacao a
     JOIN visitante v ON v.id = a.id_visitante
     LEFT JOIN empresa e ON e.id = a.id_empresa
     JOIN status_autorizacao sa ON sa.id = a.id_status_autorizacao
     JOIN setor s ON s.id = a.id_setor_solicitante
     LEFT JOIN veiculo ve ON ve.id = a.id_veiculo
     LEFT JOIN historico_autorizacao h ON h.id = (( SELECT h2.id
           FROM historico_autorizacao h2
          WHERE h2.id_autorizacao = a.id
          ORDER BY h2.data_hora
         LIMIT 1))
     LEFT JOIN usuario u ON u.id = h.id_usuario;




-- public.painel_autorizacao source

CREATE OR REPLACE VIEW public.painel_autorizacao
AS SELECT status_exibicao,
    count(*) AS quantidade
   FROM autorizacao_consulta
  GROUP BY status_exibicao;

-- Functions

CREATE OR REPLACE FUNCTION public.trg_empresa_maiusculo()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
  NEW.nome = UPPER(NEW.nome);
  NEW.cnpj = UPPER(NEW.cnpj);

  RETURN NEW;
END;
$function$
;

CREATE OR REPLACE FUNCTION public.trg_veiculo_maiusculo()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
  NEW.placa = UPPER(NEW.placa);
  NEW.cor = UPPER(NEW.cor);
  NEW.marca = UPPER(NEW.marca);
  NEW.tipo = UPPER(NEW.tipo);
  NEW.observacoes = UPPER(NEW.observacoes);

  RETURN NEW;
END;
$function$
;

CREATE OR REPLACE FUNCTION public.trg_visitante_maiusculo()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
  NEW.nome = UPPER(NEW.nome);
  NEW.email = UPPER(NEW.email);
  NEW.celular = UPPER(NEW.celular);
  NEW.rg = UPPER(NEW.rg);
  NEW.cpf = UPPER(NEW.cpf);

  RETURN NEW;
END;
$function$
;

-- Triggers

create trigger empresa_maiusculo before
insert
    or
update
    on
    public.empresa for each row execute function trg_empresa_maiusculo();

create trigger veiculo_maiusculo before
insert
    or
update
    on
    public.veiculo for each row execute function trg_veiculo_maiusculo();

create trigger visitante_maiusculo before
insert
    or
update
    on
    public.visitante for each row execute function trg_visitante_maiusculo();
