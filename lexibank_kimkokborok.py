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

        # (2) add concepts
        concepts = {}
        for concept in self.conceptlists[0].concepts.values():
            idx = concept.id.split("-")[-1] + "_" + slug(concept.english)
            args.writer.add_concept(
                ID=idx,
                Name=concept.english,
                Concepticon_ID=concept.concepticon_id,
                Concepticon_Gloss=concept.concepticon_gloss,
            )
            concepts[concept.id] = idx
        args.log.info("added concepts")

        # read in data
        data = self.raw_dir.read_csv("data.tsv", delimiter="\t", dicts=True)

        # add data
        for entry in data:
            args.writer.add_form_with_segments(
                Language_ID=entry["DOCULECT"],
                Parameter_ID=concepts["ID"],
                Value=entry["IPA"],
                Form=entry["IPA"],
                Segments=entry["TOKENS"],
                Source="Kim2011",
            )
