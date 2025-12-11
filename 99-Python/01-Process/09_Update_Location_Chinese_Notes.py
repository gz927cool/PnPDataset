import os
import pandas as pd

enrich_dir = r"c:\Users\001\Desktop\list\04-Enrich"

# Knowledge Base with Chinese Reasons
# Format: "Term": ("Location", "Chinese Reason")
kb_cn = {
    # A
    "Accademia di S. Luca": ("Rome", "罗马圣卢卡学院"),
    "Accademia del Disegno": ("Florence", "佛罗伦萨迪塞诺学院"),
    "Accademia dei Lincei": ("Rome", "罗马林琴学院"),
    "Accademia degli Umoristi": ("Rome", "罗马幽默学院"),
    "Accademia Albrizziana": ("Venice", "威尼斯阿尔布里齐亚纳学院"),
    "Accademia di Pittura e Scultura": ("Rome", "通常指罗马的法国学院或圣卢卡学院"),
    "Adam, Robert": ("London/Rome", "英国新古典主义建筑师"),
    "Adam, James": ("London/Rome", "英国建筑师，罗伯特·亚当之弟"),
    "Agucchi, Giovanni Battista": ("Rome", "博洛尼亚教士，活跃于罗马的艺术理论家"),
    "Albani, Cardinal Annibale": ("Rome", "罗马红衣主教，艺术赞助人"),
    "Albani, Francesco": ("Bologna", "博洛尼亚画派画家"),
    "Albani, Gianfrancesco (Pope Clement XI)": ("Rome", "教皇克莱门特十一世"),
    "Aldobrandini, Cardinal Pietro": ("Rome", "罗马红衣主教，重要收藏家"),
    "Aldobrandini, Ippolito (Pope Clement VIII)": ("Rome", "教皇克莱门特八世"),
    "Alexander VII": ("Rome", "教皇亚历山大七世 (Chigi家族)"),
    "Alexander VIII": ("Rome", "教皇亚历山大八世 (Ottoboni家族)"),
    "Algardi, Alessandro": ("Rome", "罗马巴洛克雕塑家"),
    "Algarotti, Francesco": ("Venice/Berlin", "威尼斯博学家，艺术鉴赏家"),
    "Amigoni, Jacopo": ("Venice", "威尼斯洛可可画家"),
    "Anne of Austria": ("Paris", "法国摄政太后"),
    "Anne, Queen of England": ("London", "英国女王"),
    "Arpino, Cavaliere d'": ("Rome", "罗马样式主义晚期画家"),
    "Arundel, Lord": ("London", "英国重要艺术收藏家"),
    
    # B
    "'Baciccio'": ("Rome", "活跃于罗马 (Gaulli)"),
    "Bernardine Baccinelli": ("Rome", "疑似 Baciccio 变体/相关"),
    "Bacon, Sir Francis": ("London", "英国哲学家/政治家"),
    "Baglione, Giovanni": ("Rome", "罗马巴洛克画家/传记作家"),
    "Bagutti, Pietro Martire": ("Bologna", "活跃于博洛尼亚的灰泥艺术家"),
    "Baldinucci, Filippo": ("Florence", "佛罗伦萨艺术史学家"),
    "Balestra, Antonio": ("Verona/Venice", "维罗纳画家"),
    "Bamboccianti": ("Rome", "活跃于罗马的风俗画家群体"),
    "Barberini family": ("Rome", "罗马显赫家族 (教皇乌尔班八世)"),
    "Barberini, Maffeo (Pope Urban VIII)": ("Rome", "教皇乌尔班八世"),
    "Barberini, Cardinal Francesco": ("Rome", "罗马红衣主教，巴贝里尼家族"),
    "Barberini, Cardinal Antonio": ("Rome", "罗马红衣主教，巴贝里尼家族"),
    "Barbieri, Giovanni Francesco (Guercino)": ("Bologna/Rome", "圭尔奇诺，活跃于博洛尼亚和罗马"),
    "Barocci, Federico": ("Urbino", "乌尔比诺画派代表"),
    "Bartoli, Pietro Santi": ("Rome", "罗马雕刻家/古董研究者"),
    "Baschenis, Evaristo": ("Bergamo", "贝加莫静物画家"),
    "Bassano, Jacopo": ("Venice", "威尼斯画派画家"),
    "Batoni, Pompeo": ("Rome", "罗马新古典主义先驱"),
    "Bellori, Giovan Pietro": ("Rome", "罗马著名艺术理论家"),
    "Bernini, Gian Lorenzo": ("Rome", "罗马巴洛克大师"),
    "Bibiena family": ("Bologna", "博洛尼亚剧院设计家族"),
    "Bombelli, Sebastiano": ("Venice", "威尼斯肖像画家"),
    "Borromini, Francesco": ("Rome", "罗马巴洛克建筑师"),
    "Boucher, François": ("Paris", "法国洛可可画家"),
    "Brandi, Giacinto": ("Rome", "罗马巴洛克画家"),
    "Burlington, Lord": ("London", "英国帕拉第奥主义建筑赞助人"),
    
    # C
    "Cagnacci, Guido": ("Bologna/Venice", "博洛尼亚画派，后活跃于威尼斯"),
    "Canaletto": ("Venice/London", "威尼斯风景画家"),
    "Canova, Antonio": ("Rome/Venice", "新古典主义雕塑家"),
    "Caracci, Agostino": ("Bologna/Rome", "卡拉奇兄弟之一，博洛尼亚学院创始人"),
    "Caracci, Annibale": ("Bologna/Rome", "卡拉奇兄弟之一，巴洛克风格先驱"),
    "Caracci, Lodovico": ("Bologna", "卡拉奇兄弟之一"),
    "Caravaggio": ("Rome", "巴洛克现实主义先驱"),
    "Carlone, Carlo": ("Como/Austria", "活跃于中欧的意大利画家"),
    "Carriera, Rosalba": ("Venice", "威尼斯粉彩肖像画家"),
    "Castiglione, Giovanni Benedetto": ("Genoa/Rome", "热那亚画家/版画家"),
    "Catherine the Great of Russia": ("St. Petersburg", "俄国女皇，重要收藏家"),
    "Cavallino, Bernardo": ("Naples", "那不勒斯画派画家"),
    "Cavedone, Giacomo": ("Bologna", "博洛尼亚画派画家"),
    "Charles I of England": ("London", "英国国王，重要收藏家"),
    "Charles II of England": ("London", "英国国王"),
    "Chigi, Agostino": ("Rome", "罗马银行家，文艺复兴赞助人"),
    "Chigi, Fabio (Pope Alexander VII)": ("Rome", "教皇亚历山大七世"),
    "Christina, Queen of Sweden": ("Rome", "瑞典女王，退位后定居罗马"),
    "Cignani, Carlo": ("Bologna", "博洛尼亚画派晚期大师"),
    "Cigoli, Lodovico": ("Florence/Rome", "佛罗伦萨巴洛克早期画家"),
    "Claude Lorrain": ("Rome", "活跃于罗马的法国风景画家"),
    "Clement VIII": ("Rome", "教皇克莱门特八世"),
    "Clement IX": ("Rome", "教皇克莱门特九世 (Rospigliosi)"),
    "Clement X": ("Rome", "教皇克莱门特十世 (Altieri)"),
    "Clement XI": ("Rome", "教皇克莱门特十一世 (Albani)"),
    "Clement XII": ("Rome", "教皇克莱门特十二世 (Corsini)"),
    "Colonna family": ("Rome", "罗马古老贵族家族"),
    "Colonna, Prince Lorenzo Onofrio": ("Rome", "科隆纳家族亲王，收藏家"),
    "Conca, Sebastiano": ("Rome/Naples", "活跃于罗马的那不勒斯画家"),
    "Cortona, Pietro da": ("Rome/Florence", "罗马巴洛克盛期大师"),
    "Crespi, Giuseppe Maria": ("Bologna", "博洛尼亚风俗画家"),
    
    # D
    "Diziani, Gaspare": ("Venice", "威尼斯洛可可画家"),
    "Dolci, Carlo": ("Florence", "佛罗伦萨巴洛克画家"),
    "Domenichino (Domenico Zampieri)": ("Rome/Bologna", "博洛尼亚画派，活跃于罗马"),
    "Doria family": ("Genoa/Rome", "热那亚/罗马显赫家族"),
    "Dughet, Gaspard": ("Rome", "活跃于罗马的风景画家 (Poussin的内弟)"),
    "Duquesnoy, François": ("Rome", "活跃于罗马的佛兰芒雕塑家"),
    
    # E
    "Edwards, Pietro": ("Venice", "威尼斯绘画修复师/行政官员"),
    "Elsheimer, Adam": ("Rome", "活跃于罗马的德国画家"),
    
    # F
    "Falcone, Aniello": ("Naples", "那不勒斯战争场面画家"),
    "Farnese family": ("Parma/Rome", "帕尔马/罗马显赫家族"),
    "Farnese, Cardinal Odoardo": ("Rome", "法尔内塞家族红衣主教，卡拉奇赞助人"),
    "Fetti, Domenico": ("Mantua/Venice", "活跃于曼图亚和威尼斯的画家"),
    "Fiammingo (Duquesnoy)": ("Rome", "即 François Duquesnoy"),
    "Fontana, Carlo": ("Rome", "罗马巴洛克晚期建筑师"),
    "Franceschini, Marcantonio": ("Bologna", "博洛尼亚画派画家"),
    "Frederick the Great": ("Berlin/Potsdam", "普鲁士国王"),
    "Fuga, Ferdinando": ("Rome/Naples", "18世纪建筑师"),
    "Furini, Francesco": ("Florence", "佛罗伦萨画家"),
    
    # G
    "Galli-Bibiena": ("Bologna", "博洛尼亚剧院设计家族"),
    "Gaulli, Giovanni Battista (Baciccio)": ("Rome", "活跃于罗马 (Gaulli)"),
    "Gentileschi, Artemisia": ("Rome/Naples", "卡拉瓦乔派女画家"),
    "Gentileschi, Orazio": ("Rome/London", "卡拉瓦乔派画家"),
    "Ghezzi, Pier Leone": ("Rome", "罗马讽刺漫画家/画家"),
    "Giaquinto, Corrado": ("Rome/Madrid", "洛可可画家"),
    "Giordano, Luca": ("Naples/Florence/Madrid", "那不勒斯多产画家"),
    "Giorgione": ("Venice", "威尼斯画派大师"),
    "Giustiniani, Marchese Vincenzo": ("Rome", "罗马银行家，卡拉瓦乔赞助人"),
    "Gonzaga family": ("Mantua", "曼图亚统治家族"),
    "Grassi, Nicola": ("Venice", "威尼斯画家"),
    "Gregory XV": ("Rome", "教皇格里高利十五世 (Ludovisi)"),
    "Guardi, Francesco": ("Venice", "威尼斯风景画家"),
    "Guardi, Gian Antonio": ("Venice", "威尼斯画家"),
    "Guercino": ("Bologna/Rome", "圭尔奇诺，博洛尼亚画派大师"),
    "Guidi, Domenico": ("Rome", "罗马巴洛克雕塑家"),
    
    # H
    "Hamilton, Gavin": ("Rome", "苏格兰新古典主义画家/考古学家，活跃于罗马"),
    "Hapsburg family": ("Vienna/Madrid", "哈布斯堡皇室"),
    
    # I
    "Innocent X": ("Rome", "教皇英诺森十世 (Pamfili)"),
    "Innocent XI": ("Rome", "教皇英诺森十一世 (Odescalchi)"),
    "Innocent XII": ("Rome", "教皇英诺森十二世 (Pignatelli)"),
    
    # J
    "Juvarra, Filippo": ("Turin", "都灵巴洛克建筑师"),
    
    # L
    "Lanfranco, Giovanni": ("Rome/Naples", "巴洛克画家，活跃于罗马和那不勒斯"),
    "Largillierre, Nicolas de": ("Paris", "法国肖像画家"),
    "Lazzarini, Gregorio": ("Venice", "威尼斯画家，Tiepolo的老师"),
    "Le Brun, Charles": ("Paris", "路易十四的首席画家"),
    "Leo XI": ("Rome", "教皇利奥十一世 (Medici)"),
    "Leopold I, Emperor": ("Vienna", "神圣罗马帝国皇帝"),
    "Liberi, Pietro": ("Venice", "威尼斯画家"),
    "Longhi, Pietro": ("Venice", "威尼斯风俗画家"),
    "Loth, Johann Carl": ("Venice", "活跃于威尼斯的德国画家"),
    "Louis XIII": ("Paris", "法国国王"),
    "Louis XIV": ("Paris", "法国国王 (太阳王)"),
    "Louis XV": ("Paris", "法国国王"),
    "Ludovisi, Cardinal Ludovico": ("Rome", "罗马红衣主教，重要收藏家"),
    "Luti, Benedetto": ("Rome", "活跃于罗马的托斯卡纳画家"),
    
    # M
    "Maderno, Carlo": ("Rome", "罗马巴洛克早期建筑师"),
    "Maffei, Scipione": ("Verona", "维罗纳学者/作家"),
    "Magnasco, Alessandro": ("Genoa/Milan", "热那亚画家，以怪诞风格著称"),
    "Manfredi, Bartolomeo": ("Rome", "卡拉瓦乔派画家"),
    "Maratta, Carlo": ("Rome", "罗马巴洛克晚期古典主义大师"),
    "Marini, Giambattista": ("Rome/Paris", "巴洛克诗人"),
    "Massimi, Cardinal Camillo": ("Rome", "罗马红衣主教，Poussin赞助人"),
    "Mazarin, Cardinal": ("Paris", "法国红衣主教/首相"),
    "Mazza, Damiano": ("Venice", "威尼斯画家"),
    "Medici family": ("Florence", "佛罗伦萨统治家族"),
    "Medici, Cardinal Leopoldo de'": ("Florence", "美第奇家族红衣主教，收藏家"),
    "Medici, Cosimo III de'": ("Florence", "托斯卡纳大公"),
    "Medici, Marie de'": ("Paris", "法国王后"),
    "Mengs, Anton Raphael": ("Rome/Madrid", "新古典主义先驱"),
    "Mola, Pier Francesco": ("Rome", "活跃于罗马的提契诺画家"),
    "Molinarolo (Baccinelli)": ("Rome", "即 Baciccio"),
    "Monsù Desiderio": ("Naples", "那不勒斯的一组画家 (François de Nomé等)"),
    "Muratori, Ludovico Antonio": ("Modena", "意大利历史学家/学者"),
    
    # N
    "Napoletano, Filippo": ("Rome/Naples", "风景画家"),
    "Neri, San Filippo": ("Rome", "奥拉托利会创始人"),
    "Newton, Sir Isaac": ("London", "英国科学家"),
    
    # O
    "Odescalchi family": ("Rome", "罗马显赫家族"),
    "Odescalchi, Benedetto (Pope Innocent XI)": ("Rome", "教皇英诺森十一世"),
    "Oratorians": ("Rome", "奥拉托利会 (天主教修会)"),
    "Orsini family": ("Rome", "罗马古老贵族家族"),
    "Ottoboni, Cardinal Pietro": ("Rome", "罗马红衣主教，重要艺术/音乐赞助人"),
    
    # P
    "Pamfili family": ("Rome", "罗马显赫家族"),
    "Pamfili, Camillo": ("Rome", "帕姆菲利家族亲王"),
    "Pamfili, Giovanni Battista (Pope Innocent X)": ("Rome", "教皇英诺森十世"),
    "Panini, Giovanni Paolo": ("Rome", "罗马维杜塔(Veduta)画家"),
    "Parodi, Filippo": ("Genoa", "热那亚巴洛克雕塑家"),
    "Pasinelli, Lorenzo": ("Bologna", "博洛尼亚画家"),
    "Passeri, Giovanni Battista": ("Rome", "罗马画家/传记作家"),
    "Paul V": ("Rome", "教皇保罗五世 (Borghese)"),
    "Pellegrini, Giovanni Antonio": ("Venice", "威尼斯洛可可画家"),
    "Peretti, Felice (Pope Sixtus V)": ("Rome", "教皇西克斯图斯五世"),
    "Piazzetta, Giovanni Battista": ("Venice", "威尼斯画家"),
    "Pietro da Cortona": ("Rome", "罗马巴洛克盛期大师"),
    "Piles, Roger de": ("Paris", "法国艺术理论家"),
    "Piranesi, Giovanni Battista": ("Rome", "威尼斯出生的罗马版画家/建筑师"),
    "Pittoni, Giambattista": ("Venice", "威尼斯画家"),
    "Poussin, Nicolas": ("Rome", "活跃于罗马的法国古典主义大师"),
    "Pozzo, Andrea": ("Rome/Vienna", "耶稣会画家/建筑师 (透视法大师)"),
    "Preti, Mattia": ("Naples/Malta", "卡拉布里亚骑士，活跃于那不勒斯"),
    "Procaccini, Giulio Cesare": ("Milan", "米兰巴洛克画家"),
    
    # R
    "Raggi, Antonio": ("Rome", "罗马巴洛克雕塑家 (Bernini学派)"),
    "Raphael": ("Rome", "文艺复兴三杰之一"),
    "Reni, Guido": ("Bologna/Rome", "博洛尼亚画派大师"),
    "Reynolds, Sir Joshua": ("London", "英国皇家艺术学院首任院长"),
    "Ribera, Jusepe de": ("Naples", "活跃于那不勒斯的西班牙画家"),
    "Riccardi family": ("Florence", "佛罗伦萨显赫家族"),
    "Ricci, Marco": ("Venice", "威尼斯风景画家"),
    "Ricci, Sebastiano": ("Venice", "威尼斯洛可可先驱"),
    "Richelieu, Cardinal": ("Paris", "法国红衣主教/首相"),
    "Rigaud, Hyacinthe": ("Paris", "法国巴洛克肖像画家"),
    "Rosa, Salvator": ("Rome/Florence", "以风景和反叛性格著称的画家"),
    "Rospigliosi family": ("Rome", "罗马/皮斯托亚家族"),
    "Rospigliosi, Giulio (Pope Clement IX)": ("Rome", "教皇克莱门特九世"),
    "Rubens, Peter Paul": ("Antwerp", "佛兰芒巴洛克大师"),
    "Rusconi, Camillo": ("Rome", "罗马巴洛克晚期雕塑家"),
    "Ruspoli, Prince Francesco Maria": ("Rome", "罗马亲王，音乐/艺术赞助人"),
    
    # S
    "Sacchi, Andrea": ("Rome", "罗马巴洛克古典主义画家"),
    "Sacchetti family": ("Rome", "罗马银行家家族"),
    "Sacchetti, Cardinal Giulio": ("Rome", "罗马红衣主教"),
    "Sandrart, Joachim von": ("Rome/Nuremberg", "德国画家/传记作家"),
    "Sassoferrato (Giovan Battista Salvi)": ("Rome", "以圣母像著称的画家"),
    "Scarlatti, Alessandro": ("Rome/Naples", "巴洛克作曲家"),
    "Sebastiano del Piombo": ("Rome", "文艺复兴画家"),
    "Serodine, Giovanni": ("Rome", "活跃于罗马的提契诺画家"),
    "Shaftesbury, Lord": ("London", "英国哲学家"),
    "Sixtus V": ("Rome", "教皇西克斯图斯五世"),
    "Smith, Joseph (Consul Smith)": ("Venice", "英国驻威尼斯领事，收藏家"),
    "Solimena, Francesco": ("Naples", "那不勒斯巴洛克晚期大师"),
    "Spada, Cardinal Bernardino": ("Rome", "罗马红衣主教"),
    "Spinola family": ("Genoa", "热那亚显赫家族"),
    "Strozzi, Bernardo": ("Genoa/Venice", "热那亚/威尼斯巴洛克画家"),
    "Subleyras, Pierre": ("Rome", "活跃于罗马的法国画家"),
    
    # T
    "Tassi, Agostino": ("Rome", "罗马风景/海景画家"),
    "Tempesta, Antonio": ("Rome", "罗马版画家/画家"),
    "Teniers, David the Younger": ("Antwerp", "佛兰芒风俗画家"),
    "Testa, Pietro": ("Rome", "罗马画家/版画家"),
    "Theatines": ("Rome", "天主教修会 (Theatines)"),
    "Tiepolo, Giambattista": ("Venice/Würzburg/Madrid", "威尼斯洛可可壁画大师"),
    "Tiepolo, Giandomenico": ("Venice", "Giambattista之子，风俗画家"),
    "Tintoretto": ("Venice", "威尼斯画派大师"),
    "Titian": ("Venice", "威尼斯画派泰斗"),
    "Trevisani, Francesco": ("Rome", "活跃于罗马的威尼斯/罗马画派画家"),
    
    # U
    "Urban VIII": ("Rome", "教皇乌尔班八世 (Barberini)"),
    
    # V
    "Vaccaro, Andrea": ("Naples", "那不勒斯画家"),
    "Valentin de Boulogne": ("Rome", "活跃于罗马的法国卡拉瓦乔派画家"),
    "Van Dyck, Anthony": ("London/Antwerp/Genoa", "佛兰芒肖像大师"),
    "Vanvitelli, Gaspare": ("Rome", "荷兰裔罗马风景画家 (Van Wittel)"),
    "Vanvitelli, Luigi": ("Naples", "卡塞塔皇宫建筑师"),
    "Vasari, Giorgio": ("Florence", "画家/建筑师/传记作家"),
    "Velasquez": ("Madrid", "西班牙巴洛克大师"),
    "Venice": ("Venice", "意大利城市"),
    "Veronese, Paolo": ("Venice", "威尼斯画派大师"),
    "Vleughels, Nicolas": ("Rome", "法国学院院长"),
    "Volterrano (Baldassarre Franceschini)": ("Florence", "佛罗伦萨巴洛克画家"),
    "Vouet, Simon": ("Rome/Paris", "法国巴洛克绘画奠基人"),
    
    # W
    "Walpole, Horace": ("London", "英国作家/艺术史学家"),
    "Watteau, Antoine": ("Paris", "法国洛可可画家"),
    "Winckelmann, Johann Joachim": ("Rome", "艺术史之父，新古典主义理论家"),
    "Wootton, John": ("London", "英国运动/风景画家"),
    "Wren, Sir Christopher": ("London", "英国建筑师 (圣保罗大教堂)"),
    
    # Z
    "Zanetti, Anton Maria": ("Venice", "威尼斯鉴赏家/版画家"),
    "Zuccarelli, Francesco": ("Venice/London", "风景画家"),
    "Zuccaro, Federico": ("Rome", "罗马样式主义晚期画家/理论家")
}

def update_files_with_cn():
    print("--- Updating Files with Chinese Notes and Reordering ---")
    files = [f for f in os.listdir(enrich_dir) if f.endswith("_refined.csv")]
    
    total_updated = 0
    
    for filename in files:
        path = os.path.join(enrich_dir, filename)
        try:
            df = pd.read_csv(path)
            
            # 1. Ensure columns exist
            if 'Proposed Location' not in df.columns:
                df['Proposed Location'] = ""
            
            # Create new column '备注/来源'
            df['备注/来源'] = ""
            
            updated_in_file = 0
            
            # 2. Update data
            for index, row in df.iterrows():
                term = str(row['Index_Main Entry']).strip()
                clean_term = term.strip("'")
                
                loc = ""
                reason_cn = ""
                
                if term in kb_cn:
                    loc, reason_cn = kb_cn[term]
                elif clean_term in kb_cn:
                    loc, reason_cn = kb_cn[clean_term]
                
                if loc:
                    df.at[index, 'Proposed Location'] = loc
                    df.at[index, '备注/来源'] = reason_cn
                    updated_in_file += 1
            
            # 3. Reorder columns
            # Target: Index_Main Entry, CIDOC_Type, Index_Location, Proposed Location, 备注/来源, ...others
            
            # Identify fixed columns
            fixed_cols = ['Index_Main Entry', 'CIDOC_Type', 'Index_Location', 'Proposed Location', '备注/来源']
            
            # Identify remaining columns (dynamic)
            remaining_cols = [c for c in df.columns if c not in fixed_cols and c != 'Notes'] # Exclude old 'Notes'
            
            # Construct new order
            new_order = fixed_cols + remaining_cols
            
            # Reorder DataFrame
            df = df[new_order]
            
            df.to_csv(path, index=False, encoding='utf-8-sig')
            print(f"Updated {filename}: {updated_in_file} entries enriched, columns reordered.")
            total_updated += 1
                
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            
    print(f"Total files processed: {total_updated}")

if __name__ == "__main__":
    update_files_with_cn()
