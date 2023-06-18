.PHONY: docs test unittest resource

PYTHON := $(shell which python)

PROJ_DIR      := .
DOC_DIR       := ${PROJ_DIR}/docs
BUILD_DIR     := ${PROJ_DIR}/build
DIST_DIR      := ${PROJ_DIR}/dist
TEST_DIR      := ${PROJ_DIR}/test
TESTFILE_DIR  := ${TEST_DIR}/testfile
DATASET_DIR   := ${TESTFILE_DIR}/dataset
SRC_DIR       := ${PROJ_DIR}/tbsync
TEMPLATES_DIR := ${PROJ_DIR}/templates
RESOURCE_DIR  := ${PROJ_DIR}/resource

RANGE_DIR      ?= .
RANGE_TEST_DIR := ${TEST_DIR}/${RANGE_DIR}
RANGE_SRC_DIR  := ${SRC_DIR}/${RANGE_DIR}

GAMES ?= arknights fgo genshin girlsfrontline azurlane

COV_TYPES ?= xml term-missing

package:
	$(PYTHON) -m build --sdist --wheel --outdir ${DIST_DIR}
clean:
	rm -rf ${DIST_DIR} ${BUILD_DIR} *.egg-info \
		$(shell find ${SRC_DIR}/games -name index.json -type f) \
		$(shell find ${SRC_DIR}/games -name danbooru_tags.json -type f) \
		$(shell find ${SRC_DIR}/games -name pixiv_names.json -type f) \
		$(shell find ${SRC_DIR}/games -name pixiv_characters.json -type f) \
		$(shell find ${SRC_DIR}/games -name pixiv_alias.yaml -type f)

test: unittest

unittest:
	UNITTEST=1 \
		pytest "${RANGE_TEST_DIR}" \
		-sv -m unittest \
		$(shell for type in ${COV_TYPES}; do echo "--cov-report=$$type"; done) \
		--cov="${RANGE_SRC_DIR}" \
		$(if ${MIN_COVERAGE},--cov-fail-under=${MIN_COVERAGE},) \
		$(if ${WORKERS},-n ${WORKERS},)

docs:
	$(MAKE) -C "${DOC_DIR}" build
pdocs:
	$(MAKE) -C "${DOC_DIR}" prod

dataset:
	mkdir -p ${DATASET_DIR}
	if [ ! -d ${DATASET_DIR}/chafen_arknights ]; then \
		git clone https://${HF_NARUGO_USERNAME}:${HF_NARUGO_PASSWORD}@huggingface.co/datasets/deepghs/chafen_arknights.git ${DATASET_DIR}/chafen_arknights; \
	fi
	if [ ! -d ${DATASET_DIR}/monochrome_danbooru ]; then \
		git clone https://${HF_NARUGO_USERNAME}:${HF_NARUGO_PASSWORD}@huggingface.co/datasets/deepghs/monochrome_danbooru.git ${DATASET_DIR}/monochrome_danbooru; \
	fi