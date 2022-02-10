CREATE TABLE news_data(
	id						bigserial not null,
	date					varchar(255),
	media					varchar(255),
	title					text,
	summary					text,
	created_on				TIMESTAMP(0) DEFAULT CURRENT_TIMESTAMP::TIMESTAMP(0)
);
