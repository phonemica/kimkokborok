import pathlib
import attr
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import progressbar as pb
from pylexibank import FormSpec


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "kimkokborok"
    writer_options = dict(keep_languages=False, keep_parameters=False)

    def cmd_makecldf(self, args):
        # (1) add bib
        args.writer.add_sources()
        args.log.info("added sources")
        
        sources = {}
        for language in self.languages:
            args.writer.add_language(
                    ID=language["ID"],
                    Name=language["Name"],
                    Glottocode=language["Glottocode"],
                    )
            sources[language["ID"]] = language["Sources"]

        # (2) add concepts
        concepts = {}
        for concept in self.concepts:
            idx = concept["NUMBER"] + "-" + slug(concept["ENGLISH"])
            args.writer.add_concept(
                    ID=idx,
                    Name=concept["ENGLISH"],
                    Concepticon_ID=concept["CONCEPTICON_ID"],
                    Concepticon_Gloss=concept["CONCEPTICON_GLOSS"]
                    )
            concepts[concept["ENGLISH"]] = idx
        args.log.info("added concepts")

        # read in data
        data = self.raw_dir.read_csv("data.tsv", delimiter="\t", dicts=True)

        # add data
        errors = set()

        for entry in data:
            if entry["SOURCE_CONCEPT"] in concepts:
                args.writer.add_form_with_segments(
                    Language_ID=entry["DOCULECT"],
                    Parameter_ID=concepts[entry["SOURCE_CONCEPT"]],
                    Value=entry["IPA"],
                    Form=entry["IPA"],
                    Segments=entry["TOKENS"].split(),
                    Source=sources[entry["DOCULECT"]],
                )
            else:
                errors.add(entry["SOURCE_CONCEPT"])
        for error in errors:
            print(error)
