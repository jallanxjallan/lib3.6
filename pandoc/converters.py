#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import pypandoc

def format_args(func):
    def wrapper(source, *output, **kwargs):
                        
        keyword_wargs = defaultdict(list)
        
        if kwargs.get('filters']:
            for filter_name in kwargs['filters']:
                f = Path(filter_name)
                keyword_wargs['filters'].append(str(filter_folder.joinpath(f).with_suffix('.py'))

        if kwargs.get('metadata']:
            for k,v in metadata.items():
                keyword_wargs['extra_args'].append(f'--metadata={k}:{v}')
        
        if len(output) > 0:
            if output[0] in pypandoc.get_pandoc_formats():
                output = output[0]
            else:
                keyword_wargs['outputfile'] = outputfile[0]
                output = None
        
        kwargs = {k:v for k,v in keyword_args.items()}
        return method(source, output, **kwargs)
    return wrapper

@format_args
def convert_text(source, *output, **kwargs):
    try:
        rs = pypandoc.convert_text(source, output, **kwargs)
    except Exception as e:
        logger.info(f'unable to import {filepath}')
        return False
    if outputfile:
        return True
    return rs
    
@format_argu
def convert_file(source, *output, **kwargs)
    
    try:
        rs = pypandoc.convert_text(source, output, **kwargs)
    except FileNotFoundError:
        logger.info(f'unable to import {filepath}')
        return False
    except RuntimeError as e:
        logger.info(f'unable to import {filepath}')
        return False
    except Exception as e:
        logger.info(f'unable to import {filepath}')
        return False
    if outputfile:
        return True
    return rs
    
"""Converts given `source` from `format` to `to`.

    :param str source: Unicode string or bytes (see encoding)

    :param str to: format into which the input should be converted; can be one of
            `pypandoc.get_pandoc_formats()[1]`

    :param str format: the format of the inputs; can be one of `pypandoc.get_pandoc_formats()[1]`

    :param list extra_args: extra arguments (list of strings) to be passed to pandoc
            (Default value = ())

    :param str encoding: the encoding of the input bytes (Default value = 'utf-8')

    :param str outputfile: output will be written to outfilename or the converted content
            returned if None (Default value = None)

    :param list filters: pandoc filters e.g. filters=['pandoc-citeproc']

    :returns: converted string (unicode) or an empty string if an outputfile was given
    :rtype: unicode

    :raises RuntimeError: if any of the inputs are not valid of if pandoc fails with an error
    :raises OSError: if pandoc is not found; make sure it has been installed and is available at
            path.
    """
    
    """Converts given `source` from `format` to `to`.

    :param str source_file: file path (see encoding)

    :param str to: format into which the input should be converted; can be one of
            `pypandoc.get_pandoc_formats()[1]`

    :param str format: the format of the inputs; will be inferred from the source_file with an
            known filename extension; can be one of `pypandoc.get_pandoc_formats()[1]`
            (Default value = None)

    :param list extra_args: extra arguments (list of strings) to be passed to pandoc
            (Default value = ())

    :param str encoding: the encoding of the file or the input bytes (Default value = 'utf-8')

    :param str outputfile: output will be written to outfilename or the converted content
            returned if None (Default value = None)

    :param list filters: pandoc filters e.g. filters=['pandoc-citeproc']

    :returns: converted string (unicode) or an empty string if an outputfile was given
    :rtype: unicode

    :raises RuntimeError: if any of the inputs are not valid of if pandoc fails with an error
    :raises OSError: if pandoc is not found; make sure it has been installed and is available at
            path.
    """
    
