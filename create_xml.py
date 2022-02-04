from lxml import etree

def create_xml(objects):
    Ads = etree.Element('Ads', {'formatVersion': '3', 'target': 'Avito.ru'})
    
    for object in objects:
        Ad = etree.SubElement(Ads, 'Ad')

        for key in object:
            newRow = etree.SubElement(Ad, key)

            if key == "Images":
                for image in object[key]:
                    Image = etree.SubElement(newRow, 'Image', {"url": image})
            else:
                newRow.text = object[key]
    
    etree.ElementTree(Ads).write('output.xml', encoding="utf-8", xml_declaration=True, pretty_print=True)
    return 'output.xml'


if __name__ == "__main__":
    create_xml(objects)